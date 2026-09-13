# DiscordBot

以 Python 與 discord.py 撰寫的 Discord 機器人，使用 Cogs 管理文字互動、活動狀態與 PTT 看板查詢功能。一般指令使用 `$` 前綴，關鍵字互動與看板查詢則直接輸入文字。

本文件依目前原始碼整理；安裝與啟動步驟尚未經實際連線驗證。現有程式的限制與待改善項目列於下方。

## 專案結構

| 路徑 | 用途 |
| --- | --- |
| `main.py` | 讀取 Token、建立機器人、載入 Cogs，並提供模組管理指令。 |
| `start.bat` | 設定終端機 UTF-8 代碼頁、切換至專案根目錄，使用 `.venv` 的 Python 啟動程式，結束後暫停視窗。 |
| `cogs/event.py` | 處理 `$Hello`、固定文字互動、主機時間與基本「看板」查詢。 |
| `cogs/crawler_ptt.py` | 抓取及解析 PTT 文章，提供看板延伸查詢與訊息格式化。 |
| `cogs/stats.py` | 連線完成時設定上線狀態與「正在玩 Python」活動。 |
| `.env` | 本機 Token 設定，需自行準備；已列入 `.gitignore`。 |
| `.gitignore` | 排除環境設定、虛擬環境與 Python 快取等檔案。 |

## 執行環境

原始碼使用 `match-case` 與 `int | None` 語法，Python 至少需要 3.10。Cog 註冊及載入流程使用 discord.py 2.x 的非同步介面。

| 套件 | 用途 |
| --- | --- |
| `discord.py` | Discord 連線、指令、事件與 Cogs。 |
| `python-dotenv` | 透過 `load_dotenv()` 讀取 `.env`。 |
| `requests` | 向 PTT 發送 HTTP 請求。 |
| `beautifulsoup4` | 以 `bs4` 匯入，解析 PTT 頁面。 |

目前專案未提供 `requirements.txt` 或套件版本鎖定檔；以下為依匯入項目整理的安裝方式，不代表已驗證所有版本組合。

## 安裝與設定

### 1. 準備 Python 環境

使用 Visual Studio Code 開啟專案資料夾，在專案根目錄開啟 PowerShell。下列新環境步驟使用 `.venv`，與目前 `start.bat` 及 `.gitignore` 的設定一致；若已有可用的同名環境，略過建立步驟。

```powershell
python --version # 確認 Python 版本至少為 3.10。
python -m venv .venv # 建立與批次檔路徑一致的虛擬環境。
.\.venv\Scripts\python.exe -m pip install "discord.py>=2,<3" python-dotenv requests beautifulsoup4 # 安裝程式匯入的套件。
```

在 Visual Studio Code 的 `Python: Select Interpreter` 選擇 `.venv\Scripts\python.exe`，讓編輯器使用相同環境。以下啟動指令直接指定虛擬環境的 Python，不需先執行啟用腳本。

啟動腳本固定使用 `.venv\Scripts\python.exe`，不會自動建立環境或安裝套件。請先完成環境準備。

### 2. 設定 Discord 機器人

在 [Discord Developer Portal](https://discord.com/developers/applications) 建立或選擇應用程式，取得 Bot Token，並將機器人加入預計使用的伺服器。目標文字頻道需允許機器人檢視頻道與傳送訊息。

目前 `main.py` 使用 `discord.Intents.all()`，因此 Bot 設定中的 Privileged Gateway Intents 需配合開啟 `Presence Intent`、`Server Members Intent` 與 `Message Content Intent`。文字前綴指令及關鍵字判斷依賴訊息內容；已驗證的應用程式可能還需要取得對應核准。設定方式請參考 [discord.py Gateway Intents 說明](https://discordpy.readthedocs.io/en/stable/intents.html#privileged-intents)。

### 3. 設定 Token

在專案根目錄的 `.env` 設定下列變數。若檔案已存在，只需確認對應設定，保留其他內容。

```dotenv
DCToken=請替換為你的Discord機器人Token # 設定機器人登入憑證，請勿公開。
```

程式以 `os.getenv("DCToken")` 取得 Token，也可由執行環境提供同名環境變數。變數名稱請維持 `DCToken`；文件中的文字僅為佔位值，不可直接用於登入。

### 4. 啟動與停止

在專案根目錄執行：

```powershell
.\start.bat # 使用專案 .venv 內的 Python 啟動機器人。
```

目前 `start.bat` 的執行流程如下：

1. 執行 `chcp 65001 >nul`，將終端機代碼頁設為 UTF-8。
2. 執行 `cd /d "%~dp0"`，切換磁碟機與工作目錄至批次檔所在的專案根目錄。
3. 將 `PYTHON` 設為 `.venv\Scripts\python.exe`，以 `"%PYTHON%" main.py %*` 啟動程式並傳遞所有參數。
4. Python 程式結束後執行 `pause`，等待按鍵，方便查看終端機輸出。

不需先執行虛擬環境的啟用腳本。若不需要批次檔的暫停行為，也可從專案根目錄直接執行：

```powershell
.\.venv\Scripts\python.exe main.py
```

登入成功時，終端機會顯示目前登入身分，狀態模組也會輸出連線訊息。可在執行中的終端機按 `Ctrl+C` 中止程式；若批次檔接著顯示暫停或中止確認提示，依畫面提示操作。

## 使用方式

### 一般指令與文字互動

| 輸入內容 | 行為 |
| --- | --- |
| `$Hello` | 回覆 `Hello, world!`；請保留大寫 `H`。 |
| `嗨` | 回覆問候文字與說明連結。 |
| `地震` | 回覆預設的玩笑文字，並非即時地震資訊。 |
| `娜塔莉` | 回覆預設角色介紹。 |
| `現在時間` | 回覆機器人執行主機的本地時間，格式為 `YYYY-MM-DD HH:MM:SS`。 |

上述無前綴的文字互動採完整字串比對，前後增加空白或其他內容不會符合相同條件。「現在時間」使用主機的 `time.localtime()`，不會依 Discord 使用者所在地轉換時區，也未在程式內固定為台灣時間。

### PTT 看板查詢

直接在頻道輸入下列文字，不需要 `$`。每次成功查詢最多傳送五篇文章，每篇各一則訊息。

| 輸入內容 | 篩選條件 | 回覆格式 |
| --- | --- | --- |
| `看板功能` | 不抓取文章，顯示功能說明。 | 指令清單。 |
| `看板` | 推文代表值大於 20。 | 僅文章網址。 |
| `看板最新` | 不限制推文代表值。 | 編號、標題連結、推文標記、作者與日期。 |
| `看板熱門` | 推文代表值大於 20。 | 同上。 |
| `看板爆文` | 推文代表值大於 99。 | 同上。 |
| `看板20` | 推文代表值大於 20。 | 同上。 |
| `看板50` | 推文代表值大於 50。 | 同上。 |

數字門檻可替換為 0 到 999 的非負整數，例如 `看板0` 只保留代表值大於 0 的文章。條件是「大於」，因此 `看板20` 不會包含代表值恰好為 20 的文章。超過 999 會收到範圍提示。

延伸查詢不得包含空白或換行，例如 `看板 20` 不會觸發查詢。以「看板」開頭但無法辨識的連續文字會收到功能提示。

### 看板來源與資料規則

- 實際請求固定為 PTT C_Chat 板的 `/bbs/C_Chat/index.html`，涵蓋動漫、遊戲與二次元綜合討論。程式雖定義其他看板路徑，目前未提供透過訊息切換看板的功能。
- 每次查詢重新抓取單一索引頁，不讀取文章內文、不翻頁，也沒有定時推播或快取。
- 文章依索引頁擷取順序反轉後回傳，並非依推文數排序；置底文章可能影響結果順序，因此「最新」不保證嚴格依發文時間排序。
- 缺少文章連結的項目會略過。日期保留頁面文字，不補上年份；格式化回覆中缺少的作者或日期顯示為「未知」。
- 推文標記「爆」以 100 作為篩選代表值；以 `X` 開頭的標記、空白或無法轉成整數的內容以 0 處理。這些代表值不等於精確推噓數，顯示時優先保留原始標記。
- 同步 HTTP 請求透過 `asyncio.to_thread()` 執行，避免直接阻塞 Discord 事件迴圈。連線與讀取逾時分別設定為 5 秒及 15 秒，並非整次請求的總時限。
- 網路或 HTTP 錯誤會回覆抓取失敗訊息；沒有符合條件的文章時會回覆「目前沒有符合條件的文章。」

## 模組管理

`main.py` 透過 `main()` 中的 `await load_extensions()` 掃描 `cogs` 目錄下的 `.py` 檔案，逐一等待模組載入，並交由非同步 `setup(bot)` 註冊 Cog。相關介面可參考 [discord.py 非同步擴充模組說明](https://discordpy.readthedocs.io/en/stable/migrating.html#extension-and-cog-loading-unloading-is-now-asynchronous)。

| 指令範例 | 用途 |
| --- | --- |
| `$load event` | 載入尚未載入的模組。 |
| `$unload event` | 卸載指定模組，停止該 Cog 的指令與監聽器。 |
| `$reload event` | 重新載入指定模組。 |

模組參數使用檔名去掉 `.py` 的名稱，可填入 `event`、`crawler_ptt` 或 `stats`，不需加上 `cogs.`。正常啟動時模組已載入，更新既有模組應使用 `$reload`。

目前這三個管理指令沒有擁有者或管理員權限檢查，能觸發指令的使用者可能改變模組狀態。此為現有程式行為，權限限制尚待實作。

## 常見問題

| 現象 | 檢查方向 |
| --- | --- |
| 顯示找不到環境變數 `DCToken`。 | 確認 `.env` 或執行環境有設定同名變數，且值不為空。 |
| 出現 `ModuleNotFoundError`。 | 確認安裝套件與啟動時使用相同的 Python；`bs4` 對應的安裝套件名稱為 `beautifulsoup4`。 |
| 以 `start.bat` 啟動時找不到 Python、套件或 `main.py`。 | 確認專案根目錄有 `.venv\Scripts\python.exe` 與 `main.py`，且套件已安裝於該虛擬環境。 |
| 「現在時間」與自己的時間不同。 | 回覆採用機器人執行主機的本地時間，請確認主機的時區設定。 |
| 無法連線並出現特權 Intent 相關錯誤。 | 檢查 Developer Portal 中允許的 Intents 是否符合程式設定。 |
| 機器人上線但沒有回覆。 | 檢查頻道權限、Message Content Intent、輸入格式，以及對應 Cog 是否載入。 |
| 查詢文章不足五篇或沒有結果。 | 僅搜尋單一索引頁，符合門檻的有效文章可能不足五篇；可使用 `看板最新` 比較。 |
| 抓取 PTT 失敗。 | 檢查終端機訊息與網路狀態；目前沒有自動重試機制。 |

## 待改善建議

以下項目來自原始碼閱讀，尚未實作：

1. 限制模組管理權限：為 `$load`、`$unload` 與 `$reload` 加上擁有者或適當權限檢查，並補上模組不存在、重複載入與載入失敗的回覆。
2. 縮小 Intents 範圍：評估功能真正需要的事件，取代目前的 `discord.Intents.all()`，減少不必要的特權設定。
3. 管理查詢設定與頻率：將固定看板及門檻移至設定，視需求加入冷卻時間或快取。目前每次查詢都會重新連線至 PTT。
4. 統一訊息來源判斷：`event.py` 僅忽略本機器人的訊息，`crawler_ptt.py` 則忽略所有機器人；建議統一規則以降低互相觸發的機會。
5. 記錄套件版本與驗證結果：建立可重現的依賴清單，並驗證登入、指令、查詢及狀態呈現。`stats.py` 雖設定活動細節、時間戳記與圖片資產欄位，實際 Discord 顯示效果仍需確認。
