"""
ComfyUI-MCP Custom Nodes
為 ComfyUI 提供 MCP (Model Context Protocol) 整合節點
"""

from .nodes.mcp_config_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 版本資訊
WEB_DIRECTORY = "./web"
__version__ = "1.0.0"
