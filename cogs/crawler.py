import asyncio  # 將同步網路請求交給背景執行緒。
from urllib.parse import urljoin  # 將文章相對路徑轉成完整網址。

import bs4  # 解析網頁並擷取文章欄位。
import requests  # 發送 HTTP 請求並提供連線錯誤類別。
from discord.ext import commands  # 定義 Discord 指令與 Cog。

url_ppt = "https://www.ptt.cc"  # PTT 網站根網址。
beauty = "/bbs/Beauty/index.html"  # 看板板首頁。
gossiping = "/bbs/Gossiping/index.html"  # 八卦板首頁。
c_chat = "/bbs/C_Chat/index.html"  # 動漫、遊戲與二次元綜合討論板。
boy_girl = "/bbs/Boy-Girl/index.html"  # 男女戀愛、感情困擾與兩性關係討論板。
sex = "/bbs/Sex/index.html"  # 不用過多說明的，大家都懂
pc_shopping = "/bbs/pc_shopping/index.html"
hardwaresale = "/bbs/HardwareSale/index.html"
tech_job = "/bbs/Tech_Job/index.html"  # 科技業職場、薪資待遇與求職心得討論板。
soft_job = "/bbs/Soft_Job/index.html"
salary = "/bbs/Salary/index.html"
macshop = "/bbs/MacShop/index.html"
makeup = "/bbs/makeup/index.html"
lifeismoney = "/bbs/Lifeismoney/index.html"  # 省錢板
stock = "/bbs/Stock/index.html"  # 股票投資、市場分析與財經新聞討論板。
car = "/bbs/car/index.html"  # 汽車資訊、購車菜單與駕駛心得討論板。
biker = "/bbs/biker/index.html"
taoyuan = "/bbs/Taoyuan/index.html"  # 桃園
kaohsiung = "/bbs/Kaohsiung/index.html"  # 高雄


def first_build_articles() -> list[dict]:  # 抓取頁面並建立後續功能共用的文章資料。
    headers = {  # 設定瀏覽器格式的請求標頭。
        "User-Agent": (  # 此標頭僅宣告用戶端身分，不會實際啟動瀏覽器。
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "  # 宣告作業系統與相容資訊。
            "AppleWebKit/537.36 (KHTML, like Gecko) "  # 宣告瀏覽器引擎資訊。
            "Chrome/131.0.0.0 Safari/537.36"  # 使用瀏覽器格式的版本資訊。
        ),  # 結束 User-Agent 設定。
    }  # 結束請求標頭設定。
    with requests.get(  # 每次呼叫重新抓取；連線或 HTTP 錯誤交由呼叫端處理。
        url_ppt + salary,
        # url_ppt + beauty,  # 拼接看板網址。
        headers=headers,  # 傳入瀏覽器格式的 User-Agent。
        cookies={"over18": "1"},  # 沿用既有年齡確認 Cookie。
        timeout=(5, 15),  # 分別設定連線與讀取等待秒數，並非整次請求的總時限。
    ) as response:  # 離開區塊時關閉回應。
        response.raise_for_status()  # 將 HTTP 失敗回應轉為例外。
        response.encoding = "utf-8"  # 以 UTF-8 解碼 PTT 頁面。
        soup = bs4.BeautifulSoup(response.text, "html.parser")  # 解析本次抓取的 HTML。
    articles = []  # 每次呼叫使用獨立清單，避免共用過期資料。
    for entry in soup.select("div.r-ent"):  # 依頁面順序處理文章。
        anchor = entry.select_one("div.title a[href]")  # 只讀取具有連結的文章標題。
        if anchor is None:  # 已刪除文章可能沒有連結。
            continue  # 跳過無法開啟的文章。
        title = anchor.get_text(strip=True)  # 取得標題並移除前後空白。
        author = entry.select_one("div.author")  # 取得作者欄位，允許缺漏。
        date = entry.select_one("div.date")  # 取得日期欄位，允許缺漏。
        nrec = entry.select_one("div.nrec")  # 取得推文標記，允許缺漏。
        push_text = nrec.get_text(strip=True) if nrec else ""  # 保留原始標記供顯示。
        if push_text == "爆":  # 爆文只提供門檻標記，無法得知精確數量。
            push_num = 100  # 以 100 作為篩選用代表值。
        elif push_text.startswith("X"):  # 負評標記沿用原程式歸零規則。
            push_num = 0  # 此數值不代表實際負評數，原標記另存於 push_text。
        else:  # 處理一般數字、空白與非預期標記。
            try:  # 嘗試轉為可運算的整數。
                push_num = int(push_text)  # 將一般數字轉為整數。
            except ValueError:  # 空白或非數字不應中斷其餘文章解析。
                push_num = 0  # 缺少有效數值時以零處理。
        articles.append(
            {  # 加入可由事件函式接收的結構化資料。
                "title": title,  # 文章標題。
                "publish_time": date.get_text(strip=True) if date else "",
                # 頁面日期，不推測年份。
                "author": author.get_text(strip=True) if author else "",
                # 作者帳號。
                "href": urljoin(url_ppt, anchor["href"]),  # 可直接開啟的完整文章網址。
                "push_num": push_num,  # 用於比較與運算的整數代表值。
                "push_text": push_text,  # 原始推文標記，供使用者辨識爆文或負評。
            }
        )  # 完成一筆文章資料。
    return articles  # 回傳未篩選的前置資料，交由其他函式執行功能運算。


async def fetch_articles(min_push: int | None = None) -> list[dict]:
    # 非同步執行前置動作與功能運算。
    # 提供 event.py 與本檔案內 Discord 事件 await 呼叫。
    articles = await asyncio.to_thread(
        first_build_articles
    )  # 取得未篩選的結構化文章資料。
    # 在背景執行前置動作，避免同步請求阻塞 Discord 事件迴圈。
    if min_push is not None:  # 有指定門檻時才執行推文數運算。
        articles = [  # 建立符合條件的新清單，保留前置資料不受影響。
            article  # 保留推文代表值嚴格大於門檻的文章。
            for article in articles  # 逐篇檢查前置動作建立的資料。
            if article["push_num"] > min_push  # 沿用原本「大於門檻」的規則。
        ]  # 結束文章篩選。
    articles.reverse()  # PTT 頁面由舊到新排列，回傳時改為最新文章優先。
    return articles  # 將運算後的結構化資料交回呼叫端。


def format_article(article: dict, number: int) -> str:  # 統一產生 Discord 顯示文字。
    push_text = article["push_text"] or str(
        article["push_num"]
    )  # 優先顯示原始推文標記。
    author = article["author"] or "未知"  # 作者欄位缺漏時提供可讀文字。
    publish_time = article["publish_time"] or "未知"  # 日期欄位缺漏時提供可讀文字。
    return (  # 回傳一篇文章的完整訊息。
        ":envelope: \r\n"  # 輸入表情符號當第一行
        f"{number}. [{article['title']}](<{article['href']}>)\r\n"
        # 第一行顯示順位與文章標題，並且整合進文章網址。
        f"推文：{push_text}｜作者：{author}｜日期：{publish_time}\r\n"  # 第二行顯示欄位。。
    )  # 結束文章顯示文字。


class crawler(commands.Cog):  # 保留既有 Cog 名稱，供擴充模組載入。
    def __init__(self, bot: commands.Bot):  # 接收目前的機器人實例。
        self.bot = bot  # 保存機器人實例供後續事件使用。

    @commands.Cog.listener()  # 監聽不含前綴符號與空格的看板延伸功能。
    async def on_message(self, message):  # 接收Discord的一般文字訊息。
        if message.author.bot:  # 忽略機器人訊息，避免互相觸發或無限回覆。
            return  # 結束機器人訊息的處理。
        content = message.content  # 保留原始訊息，供格式規則檢查。
        if content == "看板" or not content.startswith("看板"):
            # 基本指令由event.py處理。
            return  # 非延伸功能或其他訊息不由此監聽器回覆。
        if any(character.isspace() for character in content):  # 指令不得含空白或換行。
            return  # 不符合連續文字格式時不執行爬蟲。
        feature = content.removeprefix("看板")  # 取得緊接在「看板」後方的功能名稱。
        if feature == "功能":  # 顯示目前可使用的連續文字指令。
            await message.channel.send(  # 將功能說明傳回原訊息頻道。
                "可用功能：\r\n看板、看板最新、看板熱門、看板爆文、看板20\r\n"  # 列出功能範例。
                "-# 數字可自行替換，例如看板50代表推文數大於50。"  # 說明自訂門檻格式。
            )  # 完成功能說明訊息。
            return  # 說明功能不需要執行網路請求。
        min_push = None  # 「最新」預設不限制推文數。
        match feature:
            case "最新":
                min_push = None  # 保留全部有效文章。
            case "熱門":
                min_push = 20  # 設定熱門文章門檻。
            case "爆文":
                min_push = 99  # 爆文代表值為一百，因此使用九十九作門檻。
            case feature.isdecimal():
                min_push = int(feature)  # 將使用者輸入轉成推文門檻。
                if min_push > 999:  # 避免沒有實際用途的過大數值。
                    await message.channel.send(
                        "推文門檻請設定在0到999之間。"
                    )  # 提示有效範圍。
                    return  # 無效門檻不執行網路請求。
            case _:
                await message.channel.send(
                    "無法辨識此功能，請輸入看板功能查看用法。"
                )  # 提示查詢說明。
                return  # 未知功能不執行網路請求。
        # if feature == "最新":  # 取得本頁最新文章。
        #     min_push = None  # 保留全部有效文章。
        # elif feature == "熱門":  # 取得推文數大於二十的文章。
        #     min_push = 20  # 設定熱門文章門檻。
        # elif feature == "爆文":  # 取得頁面顯示為爆的文章。
        #     min_push = 99  # 爆文代表值為一百，因此使用九十九作門檻。
        # elif feature.isdecimal():  # 支援看板20、看板50等無符號數字功能。
        #     min_push = int(feature)  # 將使用者輸入轉成推文門檻。
        #     if min_push > 999:  # 避免沒有實際用途的過大數值。
        #         await message.channel.send(
        #             "推文門檻請設定在0到999之間。"
        #         )  # 提示有效範圍。
        #         return  # 無效門檻不執行網路請求。
        # else:  # 無法辨識的連續文字功能。
        #     await message.channel.send(
        #         "無法辨識此功能，請輸入看板功能查看用法。"
        #     )  # 提示查詢說明。
        #     return  # 未知功能不執行網路請求。
        try:  # 將網路失敗轉成使用者看得懂的訊息。
            articles = await fetch_articles(
                min_push=min_push
            )  # 執行所選功能的抓取與篩選。
        except requests.RequestException:  # 捕捉逾時、連線與 HTTP 狀態錯誤。
            await message.channel.send(
                f"目前無法取得PTT資料，請稍後再試。\r\n{requests.RequestException}"
            )  # 回覆抓取失敗。
            return  # 失敗時停止後續處理。
        if not articles:  # 檢查本次功能是否有符合條件的文章。
            await message.channel.send("目前沒有符合條件的文章。")  # 回覆空結果。
            return  # 避免進入空清單迴圈。
        for number, article in enumerate(
            articles[:5], start=1
        ):  # 每次最多回覆五篇文章。
            await message.channel.send(format_article(article, number))
            # 傳送格式化文章資料。


async def setup(bot: commands.Bot):  # load_extension 時由 Discord 呼叫。
    await bot.add_cog(crawler(bot))  # 註冊爬蟲 Cog 與既有指令。
