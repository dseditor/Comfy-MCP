# ComfyUI MCP Server

[中文说明](#中文說明) | [English](#english)

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

## 中文說明

ComfyUI MCP 服務器 - 通過模型上下文協議（MCP）無縫整合 AI 助手（Claude Code、Claude Desktop、Gemini CLI）與 ComfyUI。

### 功能特點

- 🎨 **ComfyUI 整合**: 通過 MCP 協議連接 AI 助手與 ComfyUI
- 🔧 **自定義節點**: 在 ComfyUI 中可視化配置 MCP 參數
- 📦 **便攜式設置**: 使用相對路徑，便於環境遷移
- 🚀 **自動啓動**: AI 助手需要時自動啓動 MCP 服務器
- ⚙️ **自動配置**: 自動安裝並配置 MCP 到 AI 助手

### 快速開始

#### 1. 啓動 ComfyUI

使用普通的啓動腳本即可（不需要特殊的 MCP 啓動器）：

\`\`\`batch
# Windows
run_nvidia_gpu.bat

# 或者使用你平時使用的任何 ComfyUI 啓動腳本
\`\`\`

#### 2. 在 ComfyUI 中配置 MCP

在工作流中添加 **MCP Config Generator** 節點：

1. 在 ComfyUI 中添加 \`MCP Config Generator\` 節點
2. 配置節點參數：
   - **workflow_file**: 選擇工作流 JSON 文件
   - **prompt_node_id**: 文本輸入節點 ID（例如 "45"）
   - **output_node_id**: 圖像輸出節點 ID（例如 "9"）
   - **comfy_url**: ComfyUI 服務器 URL（默認：\`http://127.0.0.1:8188\`）
   - **auto_install**: ✅ 啓用（首次設置時）
   - **auto_update_claude_code**: ✅ 啓用（如果使用 Claude Code）
   - **auto_update_claude_desktop**: ✅ 啓用（如果使用 Claude Desktop）
   - **auto_update_gemini_cli**: ✅ 啓用（如果使用 Gemini CLI）
3. 執行工作流

節點會自動：
- 安裝 MCP 服務器模塊
- 生成配置文件
- 更新 AI 助手配置文件

#### 3. 在 AI 助手中使用

完成！MCP 服務器會在你使用 AI 助手時自動啓動。

**在 Claude Code 或 Claude Desktop 中：**
\`\`\`
生成一張陽光花園中的貓的圖片
\`\`\`

AI 助手會自動：
1. 啓動 MCP 服務器（如果未運行）
2. 調用 ComfyUI 生成圖片
3. 返回生成的圖片

### 手動安裝（可選）

如果自動安裝不起作用，可以手動安裝：

\`\`\`batch
cd ComfyUI所在路徑/custom_nodes/ComfyUI-MCP
python -m pip install -r requirements.txt
python -m pip install -e .
\`\`\`

### 系統要求

- Python >= 3.10
- ComfyUI
- Claude Code、Claude Desktop 或 Gemini CLI

### 架構說明

本項目採用雙層架構：

\`\`\`
ComfyUI-MCP/
├── src/comfy_mcp_server/     ← MCP 服務器核心（由 AI 助手自動啓動）
├── nodes/mcp_config_node.py  ← ComfyUI 節點（用於配置）
├── workflow/                 ← 工作流 JSON 文件
├── pyproject.toml           ← 包配置
└── requirements.txt         ← 依賴項
\`\`\`

### 故障排除

**MCP 服務器無法工作？**
1. 檢查節點中是否啓用了 \`auto_install\`
2. 首次安裝後重啓 ComfyUI
3. 驗證模塊已安裝：\`python -m pip list | grep comfy-mcp-server\`

**AI 助手找不到 MCP 服務器？**
1. 檢查是否爲你的 AI 助手啓用了 \`auto_update_*\`
2. 配置後重啓 AI 助手
3. 手動檢查配置文件：
   - Claude Code: \`~/.config/claude-code/mcp.json\`
   - Claude Desktop: \`%APPDATA%/Claude/claude_desktop_config.json\`

### 許可證

MIT
