import os
import json
import subprocess
import sys


class MCPConfigGenerator:
    """
    ComfyUI Node: Generate MCP Server Configuration
    Select workflow files from workflow folder and configure MCP parameters
    Includes auto-install, Claude Code config, multi-format output, etc.
    """

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("status_text", "json_config")
    FUNCTION = "generate_config"
    CATEGORY = "MCP"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        # Get all JSON files from workflow folder
        workflow_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workflow")

        workflow_files = ["None"]
        if os.path.exists(workflow_dir):
            workflow_files = ["None"] + [
                f for f in os.listdir(workflow_dir)
                if f.endswith('.json')
            ]

        return {
            "required": {
                "workflow_file": (workflow_files,),
                "prompt_node_id": ("STRING", {
                    "default": "45",
                    "multiline": False
                }),
                "output_node_id": ("STRING", {
                    "default": "9",
                    "multiline": False
                }),
                "comfy_url": ("STRING", {
                    "default": "http://127.0.0.1:8188",
                    "multiline": False
                }),
                "max_poll_attempts": ("INT", {
                    "default": 60,
                    "min": 10,
                    "max": 300,
                    "step": 1
                }),
                "poll_interval": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "output_mode": (["url", "file"],),
                "config_format": (["ClaudeDesktop", "Gemini"],),
                "auto_install": ("BOOLEAN", {"default": False}),
                "auto_update_claude_code": ("BOOLEAN", {"default": False}),
                "auto_update_claude_desktop": ("BOOLEAN", {"default": False}),
                "auto_update_gemini_cli": ("BOOLEAN", {"default": False}),
            }
        }

    def generate_config(self, workflow_file, prompt_node_id, output_node_id,
                       comfy_url, max_poll_attempts, poll_interval, output_mode,
                       config_format, auto_install, auto_update_claude_code,
                       auto_update_claude_desktop, auto_update_gemini_cli):
        """
        Generate MCP config, update config files, auto-install module, auto-update AI configs
        """

        status_messages = []
        warnings = []

        # Get project root directory
        node_dir = os.path.dirname(os.path.dirname(__file__))

        # Determine full path of workflow file
        if workflow_file == "None":
            # Default workflow should also be in workflow folder
            workflow_path = os.path.join(node_dir, "workflow", "image_z_image_turbo.json")
            workflow_file = "image_z_image_turbo.json"
        else:
            workflow_path = os.path.join(node_dir, "workflow", workflow_file)

        # Verify workflow file exists
        if not os.path.exists(workflow_path):
            error_msg = f"Error: Workflow file not found: {workflow_path}"
            return (error_msg, "{}")

        # Get absolute path of python_embeded
        python_exe = os.path.abspath(
            os.path.join(node_dir, "..", "..", "..", "python_embeded", "python.exe")
        )

        # Check if Python exists
        if not os.path.exists(python_exe):
            error_msg = f"Error: Python not found: {python_exe}"
            return (error_msg, "{}")

        # 1. Auto-install module (if enabled)
        if auto_install:
            status_messages.append("=" * 50)
            status_messages.append("Auto-Install MCP Module")
            status_messages.append("=" * 50)
            warnings.append("⚠ Restart ComfyUI after installation to take effect!")

            install_result = self._install_module(python_exe, node_dir)
            status_messages.append(install_result)
            status_messages.append("")

        # Build MCP base configuration
        mcp_env_config = {
            "COMFY_URL": comfy_url,
            "COMFY_URL_EXTERNAL": comfy_url,
            "COMFY_WORKFLOW_JSON_FILE": workflow_path,
            "PROMPT_NODE_ID": str(prompt_node_id),
            "OUTPUT_NODE_ID": str(output_node_id),
            "OUTPUT_MODE": output_mode,
            "COMFY_MAX_POLL_ATTEMPTS": str(max_poll_attempts),
            "COMFY_POLL_INTERVAL": str(poll_interval)
        }

        # Generate configuration based on format
        if config_format == "ClaudeDesktop":
            mcp_config = {
                "mcpServers": {
                    "comfyui-image-generator": {
                        "command": python_exe,
                        "args": ["-m", "comfy_mcp_server"],
                        "cwd": node_dir,
                        "env": mcp_env_config
                    }
                }
            }
        else:  # Gemini
            mcp_config = {
                "mcp_servers": {
                    "comfyui-image-generator": {
                        "command": python_exe,
                        "args": ["-m", "comfy_mcp_server"],
                        "cwd": node_dir,
                        "env": mcp_env_config
                    }
                }
            }

        # 2. Auto-update AI platform configs (if enabled)
        if auto_update_claude_code:
            status_messages.append("=" * 50)
            status_messages.append("Auto-Update: Claude Code (User Scope)")
            status_messages.append("=" * 50)

            claude_code_config = {
                "command": python_exe,
                "args": ["-m", "comfy_mcp_server"],
                "cwd": node_dir,
                "env": mcp_env_config
            }

            result = self._update_claude_code(claude_code_config)
            status_messages.append(result)
            status_messages.append("")

        if auto_update_claude_desktop:
            status_messages.append("=" * 50)
            status_messages.append("Auto-Update: Claude Desktop")
            status_messages.append("=" * 50)

            claude_desktop_config = {
                "command": python_exe,
                "args": ["-m", "comfy_mcp_server"],
                "cwd": node_dir,
                "env": mcp_env_config
            }

            result = self._update_claude_desktop(claude_desktop_config)
            status_messages.append(result)
            status_messages.append("")

        if auto_update_gemini_cli:
            status_messages.append("=" * 50)
            status_messages.append("Auto-Update: Gemini CLI")
            status_messages.append("=" * 50)

            gemini_config = {
                "command": python_exe,
                "args": ["-m", "comfy_mcp_server"],
                "env": mcp_env_config,
                "timeout": 120000,
                "trust": False
            }

            result = self._update_gemini_cli(gemini_config)
            status_messages.append(result)
            status_messages.append("")

        # 3. Save JSON config file
        if config_format == "ClaudeDesktop":
            json_filename = f"claude_desktop_mcp_config_{workflow_file.replace('.json', '')}.json"
        else:
            json_filename = f"gemini_settings_{workflow_file.replace('.json', '')}.json"

        json_path = os.path.join(node_dir, json_filename)

        try:

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(mcp_config, f, indent=2, ensure_ascii=False)

            status_messages.append("=" * 50)
            status_messages.append("Configuration File Generated")
            status_messages.append("=" * 50)
            status_messages.append(f"✓ {json_filename} generated")
            status_messages.append(f"  Location: {json_path}")
            status_messages.append("")

            # 4. Update mcp_config.ini config file
            config_ini_path = os.path.join(node_dir, "mcp_config.ini")
            try:
                with open(config_ini_path, 'w', encoding='utf-8') as f:
                    f.write(f"WORKFLOW_FILE={workflow_path}\n")
                    f.write(f"PROMPT_NODE_ID={prompt_node_id}\n")
                    f.write(f"OUTPUT_NODE_ID={output_node_id}\n")
                    f.write(f"COMFY_URL={comfy_url}\n")
                    f.write(f"OUTPUT_MODE={output_mode}\n")
                    f.write(f"MAX_POLL_ATTEMPTS={max_poll_attempts}\n")
                    f.write(f"POLL_INTERVAL={poll_interval}\n")
                status_messages.append("✓ mcp_config.ini updated")
            except Exception as e:
                status_messages.append(f"⚠ Failed to update mcp_config.ini: {e}")

            # 5. Check MCP status
            status_messages.append("")
            status_messages.append("=" * 50)
            status_messages.append("MCP Status Check")
            status_messages.append("=" * 50)

            mcp_status = self._check_mcp_status(python_exe, node_dir)
            status_messages.append(mcp_status)

            # 6. Generate configuration summary
            status_messages.append("")
            status_messages.append("=" * 50)
            status_messages.append("Configuration Summary")
            status_messages.append("=" * 50)
            status_messages.append(f"Workflow: {workflow_file}")
            status_messages.append(f"Prompt Node ID: {prompt_node_id}")
            status_messages.append(f"Output Node ID: {output_node_id}")
            status_messages.append(f"ComfyUI URL: {comfy_url}")
            status_messages.append(f"Output Mode: {output_mode}")
            status_messages.append(f"Config Format: {config_format}")
            status_messages.append(f"Auto Install: {'Yes' if auto_install else 'No'}")
            status_messages.append(f"Auto Update Claude Code: {'Yes' if auto_update_claude_code else 'No'}")
            status_messages.append(f"Auto Update Claude Desktop: {'Yes' if auto_update_claude_desktop else 'No'}")
            status_messages.append(f"Auto Update Gemini CLI: {'Yes' if auto_update_gemini_cli else 'No'}")

            # 7. Add usage instructions
            if config_format == "ClaudeDesktop":
                status_messages.append("")
                status_messages.append("=" * 50)
                status_messages.append("Claude Desktop Configuration Guide")
                status_messages.append("=" * 50)
                status_messages.append("Merge generated JSON content to:")
                status_messages.append("Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
                status_messages.append("macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
            else:  # Gemini
                status_messages.append("")
                status_messages.append("=" * 50)
                status_messages.append("Gemini Configuration Guide")
                status_messages.append("=" * 50)
                status_messages.append("Add generated JSON content to Gemini's settings.json")

            # 8. Add warnings
            if warnings:
                status_messages.append("")
                status_messages.append("=" * 50)
                status_messages.append("Important Notice")
                status_messages.append("=" * 50)
                for warning in warnings:
                    status_messages.append(warning)

            # Combine final output
            final_status = "\n".join(status_messages)
            json_output = json.dumps(mcp_config, indent=2, ensure_ascii=False)

            return (final_status, json_output)

        except Exception as e:
            error_msg = f"Error: Cannot generate config file - {str(e)}"
            return (error_msg, "{}")

    def _install_module(self, python_exe, node_dir):
        """Install MCP module"""
        try:
            # Install hatchling
            result = subprocess.run(
                [python_exe, "-m", "pip", "install", "hatchling", "--quiet"],
                capture_output=True,
                text=True,
                cwd=node_dir
            )

            # Install comfy-mcp-server
            result = subprocess.run(
                [python_exe, "-m", "pip", "install", "-e", "."],
                capture_output=True,
                text=True,
                cwd=node_dir
            )

            if result.returncode == 0:
                # Verify installation
                verify_result = subprocess.run(
                    [python_exe, "-m", "comfy_mcp_server", "--help"],
                    capture_output=True,
                    text=True,
                    cwd=node_dir
                )

                if verify_result.returncode == 0:
                    return "✓ MCP module installed successfully and can run properly"
                else:
                    return "⚠ Module installed but cannot execute, may need to check environment"
            else:
                return f"✗ Installation failed: {result.stderr}"

        except Exception as e:
            return f"✗ Error during installation: {str(e)}"

    def _update_claude_code(self, config):
        """Auto-update Claude Code MCP configuration (User Scope)"""
        try:
            json_str = json.dumps(config)
            # Escape double quotes in JSON string
            json_str_escaped = json_str.replace('"', '\\"')

            # Windows requires shell=True to execute .cmd files
            cmd = f'claude mcp add-json --scope user comfyui-image-generator "{json_str_escaped}"'
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                timeout=30
            )

            if result.returncode == 0:
                return "✓ Successfully added/updated MCP configuration to Claude Code (User Scope)"
            else:
                return f"✗ Failed to update Claude Code: {result.stderr}\n  Hint: Please ensure Claude Code CLI is installed"

        except FileNotFoundError:
            return "✗ Claude Code CLI not found. Please install Claude Code first"
        except subprocess.TimeoutExpired:
            return "✗ Claude Code update timeout (network may be slow)"
        except Exception as e:
            return f"✗ Error updating Claude Code: {str(e)}"

    def _update_claude_desktop(self, config):
        """Auto-update Claude Desktop config file"""
        try:
            # Get username
            username = os.getenv('USERNAME') or os.getenv('USER')
            if not username:
                return "✗ Cannot determine username for Claude Desktop config path"

            # Claude Desktop config path
            config_path = os.path.join(
                "C:", "Users", username, "AppData", "Roaming", "Claude", "claude_desktop_config.json"
            )

            # Check if config file exists
            if not os.path.exists(config_path):
                # Create directory and initial config
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                existing_config = {"mcpServers": {}}
            else:
                # Read existing config
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)

            # Ensure mcpServers key exists
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}

            # Update or add comfyui-image-generator config
            existing_config["mcpServers"]["comfyui-image-generator"] = config

            # Write back to file
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)

            return f"✓ Successfully updated Claude Desktop config\n  Path: {config_path}"

        except PermissionError:
            return f"✗ Permission denied: Cannot write to {config_path}"
        except Exception as e:
            return f"✗ Error updating Claude Desktop config: {str(e)}"

    def _update_gemini_cli(self, config):
        """Auto-update Gemini CLI config file"""
        try:
            # Get username
            username = os.getenv('USERNAME') or os.getenv('USER')
            if not username:
                return "✗ Cannot determine username for Gemini CLI config path"

            # Gemini CLI config path
            config_path = os.path.join(
                "C:", "Users", username, ".gemini", "settings.json"
            )

            # Check if config file exists
            if not os.path.exists(config_path):
                # Create directory and initial config
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                existing_config = {"mcpServers": {}}
            else:
                # Read existing config
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)

            # Ensure mcpServers key exists
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}

            # Update or add comfyui-image-generator config
            existing_config["mcpServers"]["comfyui-image-generator"] = config

            # Write back to file
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)

            return f"✓ Successfully updated Gemini CLI config\n  Path: {config_path}"

        except PermissionError:
            return f"✗ Permission denied: Cannot write to {config_path}"
        except Exception as e:
            return f"✗ Error updating Gemini CLI config: {str(e)}"

    def _check_mcp_status(self, python_exe, node_dir):
        """Check MCP module status"""
        status_lines = []

        # 1. Check if module is installed
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "show", "comfy-mcp-server"],
                capture_output=True,
                text=True,
                cwd=node_dir
            )

            if result.returncode == 0:
                status_lines.append("✓ MCP module is installed")

                # Get version info
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        status_lines.append(f"  Version: {line.split(':', 1)[1].strip()}")
                        break
            else:
                status_lines.append("✗ MCP module is not installed")
        except Exception as e:
            status_lines.append(f"✗ Error checking module installation: {str(e)}")

        # 2. Check if module can be executed
        try:
            # Test if module can be loaded
            src_path = os.path.join(node_dir, "src")
            verify_result = subprocess.run(
                [python_exe, "-c",
                 f"import sys; sys.path.insert(0, r'{src_path}'); from comfy_mcp_server import mcp; print('OK')"],
                capture_output=True,
                text=True,
                cwd=node_dir
            )

            if verify_result.returncode == 0 and "OK" in verify_result.stdout:
                status_lines.append("✓ MCP module can be loaded successfully")
            else:
                status_lines.append("✗ MCP module cannot be loaded")
                if verify_result.stderr:
                    status_lines.append(f"  Error: {verify_result.stderr.strip()[:100]}")
        except Exception as e:
            status_lines.append(f"✗ Error testing module: {str(e)}")

        # 3. Check Claude Code MCP config (handle safely)
        try:
            # Windows requires shell=True to execute .cmd files
            claude_result = subprocess.run(
                "claude mcp list",
                capture_output=True,
                text=True,
                timeout=30,
                shell=True
            )

            if claude_result.returncode == 0:
                if "comfyui-image-generator" in claude_result.stdout:
                    status_lines.append("✓ Claude Code MCP is configured")
                else:
                    status_lines.append("ℹ Claude Code MCP is not configured")
            else:
                status_lines.append("ℹ Claude Code CLI error")
        except FileNotFoundError:
            status_lines.append("ℹ Claude Code CLI not found (optional)")
        except subprocess.TimeoutExpired:
            status_lines.append("ℹ Claude Code CLI timeout (network may be slow, but MCP might still work)")
        except Exception as e:
            status_lines.append(f"ℹ Cannot check Claude Code status (but MCP might still work)")

        return "\n".join(status_lines)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "MCPConfigGenerator": MCPConfigGenerator
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "MCPConfigGenerator": "MCP Config Generator"
}
