# ComfyUI-MCP

繁體中文 | [English](README.md)

## ComfyUI-MCP 節點介紹

首先你必須要跑通一次 ZImage 的工作流，跑通過範本的就好。

在 ComfyUI Manager 中，搜尋 MCP：

![MCP Manager](readme/mcp01.jpg)

這邊已經安裝就會出現更新、切換版本、刪除以及反安裝的圖案，那如果沒有安裝過，點取「Install」，接著，就會提醒你重新啟動 ComfyUI。

MCP 安裝完成之後，接著直接使用工作流，載入工作流 JSON 檔案（[`example/mcp.json`](example/mcp.json)），應該會是這樣一張圖。

假使你是手動加入節點，而非使用工作流，從 `auto_install` 下面的預設值都是關閉，這邊請最少要把 `Auto_install` 打開，同時把 `Workflow_File` 設定為 `Image_Z_turbo`，這個預設值，然後按下工作流的執行，跑通一次工作流。

![MCP Node Setup](readme/mcp02.jpg)

`Auto_install` 完成後，重新啟動 ComfyUI。

## 參數說明

我們解釋一下上面的參數：

- **workflow_file**: 選擇工作流 JSON 文件，這裡你可以把任何工作流匯出成 API，丟到節點的 workflow 資料夾去，就可以在這裡選擇，但要注意的是要是 T2I 的工作流，因為目前只支援文生圖。
- **prompt_node_id**: 文本輸入節點 ID（例如 "45"）
- **output_node_id**: 圖像輸出節點 ID（例如 "9"）

上面這兩個可以先不用管他，但如果你自訂 API，可以修改節點 ID 哪一個是文本哪一個是圖像輸出的 SaveImage。

- **comfy_url**: ComfyUI 服務器 URL（默認：`http://127.0.0.1:8188`）
- **auto_install**: ✅ 啓用（首次設置時）

第一次設定時必然要開啟，不然完全無法使用 MCP。

- **auto_update_claude_code**: ✅ 啓用（如果使用 Claude Code）
- **auto_update_claude_desktop**: ✅ 啓用（如果使用 Claude Desktop）
- **auto_update_gemini_cli**: ✅ 啓用（如果使用 Gemini CLI）

這幾個項目打開後，它會自動搜尋你的使用者資料夾設定，並且安裝到 CLI 與 Claude Code，工作流更新時，MCP 也會隨之更新，如果沒有安裝 Claude Code 或相關系列，只有 Gemini，上面關於 Claude 的項目，以及 MCP 這段的檢查會失敗，可以忽視它。

## 其他參數

poll 相關的參數是指檢查幾次，以及等待時間的秒數長度，如果你的 GPU 很慢生圖時間很長，就要拉長這個長度跟次數，基本上是每兩秒檢查 1 次，檢查 60 次。

`output_mode` 預設是網址，這是為了減少 token 使用，如果希望你的 Claude Desktop 能夠直接出現圖片給你看，那這邊就要改成 webp。

那正確安裝完成後，最重要的就是這個訊息：

![Installation Success](readme/mcp03.jpg)

重點是要確認 MCP 已經正確安裝在 ComfyUI 系統中，那讓我們看看 MCP 的運作情況，以 Gemini-CLI 來說就是，啟動後打入 `/mcp` 確認狀態，你會看到：

![MCP Status](readme/mcp04.jpg)

這樣就表示你的 MCP 已經開始準備要產生圖片。

那之後每次 ComfyUI 啟動後，你的 MCP 就會隨著 ComfyUI 自己啟動，我們可以試著讓 MCP 做些工作，如做一組美女月曆，Gemini-CLI 知道你需要月曆的圖片，它就會直接產生：

![Calendar Generation](readme/mcp05.jpg)

過程中它會使用 ComfyUI 產生月曆所需的圖片，將版型調整一下就會變成：

![Calendar Result](readme/mcp06.jpg)

就這樣，你的網頁素材都可以透過 ZImage 產生，只要用 ComfyUI-MCP + Gemini-CLI 就行了。
