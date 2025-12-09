from mcp.server.fastmcp import FastMCP, Context
from mcp.types import ImageContent, TextContent
import json
import urllib
from urllib import request
import time
import os
import sys
import warnings
from io import BytesIO
from PIL import Image

# Suppress warnings to avoid polluting MCP stdout
warnings.filterwarnings("ignore")

# Ensure all logging goes to stderr, not stdout
import logging
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

mcp = FastMCP("Comfy MCP Server")

host = os.environ.get("COMFY_URL")
override_host = os.environ.get("COMFY_URL_EXTERNAL")
if override_host is None:
    override_host = host
workflow = os.environ.get("COMFY_WORKFLOW_JSON_FILE")

prompt_template = json.load(
    open(workflow, "r")
) if workflow is not None else None

prompt_node_id = os.environ.get("PROMPT_NODE_ID")
output_node_id = os.environ.get("OUTPUT_NODE_ID")
output_mode = os.environ.get("OUTPUT_MODE")

# Configurable timeout settings
max_poll_attempts = int(os.environ.get("COMFY_MAX_POLL_ATTEMPTS", "60"))  # Default 60 attempts
poll_interval = int(os.environ.get("COMFY_POLL_INTERVAL", "2"))  # Default 2 seconds

ollama_api_base = os.environ.get("OLLAMA_API_BASE")
prompt_llm = os.environ.get("PROMPT_LLM")


def get_file_url(server: str, url_values: str) -> str:
    return f"{server}/view?{url_values}"


if ollama_api_base is not None and prompt_llm is not None:
    @mcp.tool()
    def generate_prompt(topic: str, ctx: Context) -> str:
        """Write an image generation prompt for a provided topic"""

        model = ChatOllama(base_url=ollama_api_base, model=prompt_llm)
        prompt = PromptTemplate.from_template("""You are an AI Image Generation Prompt Assistant.
        Your job is to review the topic provided by the user for an image generation task and create
        an appropriate prompt from it. Repond with a single prompt. Don't ask for feedback about the prompt. 

        Topic: {topic}
        Prompt: """)
        chain = prompt | model | StrOutputParser()
        response = chain.invoke({"topic": topic})
        return response


@mcp.tool()
def generate_image(prompt: str, ctx: Context) -> list[TextContent | ImageContent]:
    """Generate an image using ComfyUI workflow"""

    prompt_template[prompt_node_id]['inputs']['text'] = prompt
    p = {"prompt": prompt_template}
    data = json.dumps(p).encode('utf-8')
    req = request.Request(f"{host}/prompt", data)
    resp = request.urlopen(req)
    response_ready = False
    override_file_url = None
    image_data = None

    if resp.status == 200:
        ctx.info("Submitted prompt")
        resp_data = json.loads(resp.read())
        prompt_id = resp_data["prompt_id"]

        for t in range(0, max_poll_attempts):
            history_req = request.Request(
                f"{host}/history/{prompt_id}")
            history_resp = request.urlopen(history_req)
            if history_resp.status == 200:
                ctx.info(f"Checking status... (attempt {t+1}/{max_poll_attempts})")
                history_resp_data = json.loads(history_resp.read())
                if prompt_id in history_resp_data:
                    status = (
                        history_resp_data[prompt_id]['status']['completed']
                    )
                    if status:
                        output_data = (
                            history_resp_data[prompt_id]
                            ['outputs'][output_node_id]['images'][0]
                        )
                        url_values = urllib.parse.urlencode(output_data)
                        file_url = get_file_url(host, url_values)
                        override_file_url = get_file_url(
                            override_host, url_values)
                        file_req = request.Request(file_url)
                        file_resp = request.urlopen(file_req)
                        if file_resp.status == 200:
                            ctx.info("Image generated")
                            image_data = file_resp.read()
                            response_ready = True
                        break
                    else:
                        time.sleep(poll_interval)
                else:
                    time.sleep(poll_interval)

    if response_ready and override_file_url and image_data:
        import base64

        # Save image locally for Claude Code to access
        local_save_dir = os.environ.get("COMFY_LOCAL_SAVE_DIR", "./generated_images")
        os.makedirs(local_save_dir, exist_ok=True)

        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Convert PNG to WebP for smaller file size
        try:
            # Open the PNG image
            png_image = Image.open(BytesIO(image_data))

            # Save as WebP locally
            local_filename = f"image_{timestamp}.webp"
            local_path = os.path.abspath(os.path.join(local_save_dir, local_filename))
            png_image.save(local_path, format='WebP', quality=85, method=6)

            # Calculate size reduction
            original_size_kb = len(image_data) / 1024
            webp_size_kb = os.path.getsize(local_path) / 1024
            reduction_percent = ((original_size_kb - webp_size_kb) / original_size_kb) * 100

            ctx.info(f"Saved to {local_path}: {original_size_kb:.1f}KB -> {webp_size_kb:.1f}KB ({reduction_percent:.1f}% reduction)")

            return [
                TextContent(
                    type="text",
                    text=f"Image generated successfully!\n\n"
                         f"Remote URL: {override_file_url}\n"
                         f"Local Path: {local_path}\n"
                         f"Size: {original_size_kb:.1f}KB (PNG) -> {webp_size_kb:.1f}KB (WebP)\n"
                         f"Compression: {reduction_percent:.1f}% smaller\n\n"
                         f"You can read the image from the local path using the Read tool."
                )
            ]
        except Exception as e:
            ctx.error(f"WebP conversion failed: {e}, falling back to PNG")
            # Fallback to PNG if WebP conversion fails
            local_filename = f"image_{timestamp}.png"
            local_path = os.path.abspath(os.path.join(local_save_dir, local_filename))
            with open(local_path, 'wb') as f:
                f.write(image_data)

            image_size_kb = len(image_data) / 1024
            return [
                TextContent(
                    type="text",
                    text=f"Image generated successfully!\n\n"
                         f"Remote URL: {override_file_url}\n"
                         f"Local Path: {local_path}\n"
                         f"Size: {image_size_kb:.1f}KB (PNG)\n\n"
                         f"You can read the image from the local path using the Read tool."
                )
            ]
    else:
        return [TextContent(type="text", text="Failed to generate image. Please check server logs.")]


def run_server():
    errors = []
    if host is None:
        errors.append("- COMFY_URL environment variable not set")
    if workflow is None:
        errors.append(
            "- COMFY_WORKFLOW_JSON_FILE environment variable not set")
    if prompt_node_id is None:
        errors.append("- PROMPT_NODE_ID environment variable not set")
    if output_node_id is None:
        errors.append("- OUTPUT_NODE_ID environment variable not set")

    if len(errors) > 0:
        import sys
        errors = ["Failed to start Comfy MCP Server:"] + errors
        sys.stderr.write("\n".join(errors) + "\n")
        sys.exit(1)
    else:
        mcp.run()


if __name__ == "__main__":
    run_server()
