# ComfyUI MCP Server

[中文说明](#中文说明) | [English](#english)

---

## English

MCP Server for ComfyUI - Seamlessly integrate AI assistants (Claude Code, Claude Desktop, Gemini CLI) with ComfyUI through the Model Context Protocol.

### Features

- 🎨 **ComfyUI Integration**: Connect AI assistants to ComfyUI via MCP protocol
- 🔧 **Custom Node**: Configure MCP parameters visually within ComfyUI
- 📦 **Portable Setup**: Use relative paths for easy environment migration
- 🚀 **Auto-Start**: MCP Server launches automatically when AI assistants need it
- ⚙️ **Auto-Configuration**: Automatically install and configure MCP for AI assistants

### Quick Start

#### 1. Start ComfyUI

Simply start ComfyUI with your normal startup script (no special MCP launcher needed):

\`\`\`batch
# Windows
run_nvidia_gpu.bat

# Or any other ComfyUI startup script you normally use
\`\`\`

#### 2. Configure MCP in ComfyUI

Add the **MCP Config Generator** node to your workflow:

1. Add \`MCP Config Generator\` node in ComfyUI
2. Configure the node parameters:
   - **workflow_file**: Select your workflow JSON file
   - **prompt_node_id**: Node ID for text input (e.g., "45")
   - **output_node_id**: Node ID for image output (e.g., "9")
   - **comfy_url**: ComfyUI server URL (default: \`http://127.0.0.1:8188\`)
   - **auto_install**: ✅ Enable (for first-time setup)
   - **auto_update_claude_code**: ✅ Enable (if using Claude Code)
   - **auto_update_claude_desktop**: ✅ Enable (if using Claude Desktop)
   - **auto_update_gemini_cli**: ✅ Enable (if using Gemini CLI)
3. Execute the workflow

The node will automatically:
- Install the MCP server module
- Generate configuration files
- Update AI assistant configuration files

#### 3. Use with AI Assistants

That's it! The MCP server will automatically start when you use the AI assistant.

**In Claude Code or Claude Desktop:**
\`\`\`
Generate an image of a cat in a sunny garden
\`\`\`

The AI assistant will automatically:
1. Start the MCP server (if not running)
2. Call ComfyUI to generate the image
3. Return the generated image

### Manual Installation (Optional)

If auto-installation doesn't work, you can install manually:

\`\`\`batch
cd path/to/ComfyUI/custom_nodes/ComfyUI-MCP
python -m pip install -r requirements.txt
python -m pip install -e .
\`\`\`

### System Requirements

- Python >= 3.10
- ComfyUI
- Claude Code, Claude Desktop, or Gemini CLI

### Architecture

This project uses a dual-layer architecture:

\`\`\`
ComfyUI-MCP/
├── src/comfy_mcp_server/     ← MCP Server core (auto-started by AI assistants)
├── nodes/mcp_config_node.py  ← ComfyUI node (for configuration)
├── workflow/                 ← Workflow JSON files
├── pyproject.toml           ← Package configuration
└── requirements.txt         ← Dependencies
\`\`\`

### Troubleshooting

**MCP server not working?**
1. Check that \`auto_install\` is enabled in the node
2. Restart ComfyUI after first installation
3. Verify the module is installed: \`python -m pip list | grep comfy-mcp-server\`

**AI assistant can't find MCP server?**
1. Check that \`auto_update_*\` is enabled for your AI assistant
2. Restart the AI assistant after configuration
3. Manually check the configuration file:
   - Claude Code: \`~/.config/claude-code/mcp.json\`
   - Claude Desktop: \`%APPDATA%/Claude/claude_desktop_config.json\`

### License

MIT

---

## 中文说明

ComfyUI MCP 服务器 - 通过模型上下文协议（MCP）无缝整合 AI 助手（Claude Code、Claude Desktop、Gemini CLI）与 ComfyUI。

### 功能特点

- 🎨 **ComfyUI 整合**: 通过 MCP 协议连接 AI 助手与 ComfyUI
- 🔧 **自定义节点**: 在 ComfyUI 中可视化配置 MCP 参数
- 📦 **便携式设置**: 使用相对路径，便于环境迁移
- 🚀 **自动启动**: AI 助手需要时自动启动 MCP 服务器
- ⚙️ **自动配置**: 自动安装并配置 MCP 到 AI 助手

### 快速开始

#### 1. 启动 ComfyUI

使用普通的启动脚本即可（不需要特殊的 MCP 启动器）：

\`\`\`batch
# Windows
run_nvidia_gpu.bat

# 或者使用你平时使用的任何 ComfyUI 启动脚本
\`\`\`

#### 2. 在 ComfyUI 中配置 MCP

在工作流中添加 **MCP Config Generator** 节点：

1. 在 ComfyUI 中添加 \`MCP Config Generator\` 节点
2. 配置节点参数：
   - **workflow_file**: 选择工作流 JSON 文件
   - **prompt_node_id**: 文本输入节点 ID（例如 "45"）
   - **output_node_id**: 图像输出节点 ID（例如 "9"）
   - **comfy_url**: ComfyUI 服务器 URL（默认：\`http://127.0.0.1:8188\`）
   - **auto_install**: ✅ 启用（首次设置时）
   - **auto_update_claude_code**: ✅ 启用（如果使用 Claude Code）
   - **auto_update_claude_desktop**: ✅ 启用（如果使用 Claude Desktop）
   - **auto_update_gemini_cli**: ✅ 启用（如果使用 Gemini CLI）
3. 执行工作流

节点会自动：
- 安装 MCP 服务器模块
- 生成配置文件
- 更新 AI 助手配置文件

#### 3. 在 AI 助手中使用

完成！MCP 服务器会在你使用 AI 助手时自动启动。

**在 Claude Code 或 Claude Desktop 中：**
\`\`\`
生成一张阳光花园中的猫的图片
\`\`\`

AI 助手会自动：
1. 启动 MCP 服务器（如果未运行）
2. 调用 ComfyUI 生成图片
3. 返回生成的图片

### 手动安装（可选）

如果自动安装不起作用，可以手动安装：

\`\`\`batch
cd ComfyUI所在路径/custom_nodes/ComfyUI-MCP
python -m pip install -r requirements.txt
python -m pip install -e .
\`\`\`

### 系统要求

- Python >= 3.10
- ComfyUI
- Claude Code、Claude Desktop 或 Gemini CLI

### 架构说明

本项目采用双层架构：

\`\`\`
ComfyUI-MCP/
├── src/comfy_mcp_server/     ← MCP 服务器核心（由 AI 助手自动启动）
├── nodes/mcp_config_node.py  ← ComfyUI 节点（用于配置）
├── workflow/                 ← 工作流 JSON 文件
├── pyproject.toml           ← 包配置
└── requirements.txt         ← 依赖项
\`\`\`

### 故障排除

**MCP 服务器无法工作？**
1. 检查节点中是否启用了 \`auto_install\`
2. 首次安装后重启 ComfyUI
3. 验证模块已安装：\`python -m pip list | grep comfy-mcp-server\`

**AI 助手找不到 MCP 服务器？**
1. 检查是否为你的 AI 助手启用了 \`auto_update_*\`
2. 配置后重启 AI 助手
3. 手动检查配置文件：
   - Claude Code: \`~/.config/claude-code/mcp.json\`
   - Claude Desktop: \`%APPDATA%/Claude/claude_desktop_config.json\`

### 许可证

MIT
