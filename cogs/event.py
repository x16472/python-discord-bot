import platform
import time

import discord
import requests  # 捕捉爬蟲連線錯誤。
from discord.ext import commands

from cogs.crawler_ptt import fetch_articles  # 匯入非同步爬蟲。


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def Hello(self, ctx: commands.Context):
        await ctx.send("Hello, world!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        # 使用 match-case 判斷訊息內容
        match message.content:
            case "嗨":
                await message.channel.send(
                    "早安您好\r\n-# 今天過得好嗎?"
                    "[了解更多](<https://support.discord.com/hc/zh-tw/>)"
                )
            case "地震":
                await message.channel.send(
                    "-# 由於均均總是跌倒造成臺灣地震，已遭中華民國官方永久驅逐出境• "
                    "[了解更多](<https://support.discord.com/hc/zh-tw/>)"
                )
            case "娜塔莉":
                await message.channel.send(
                    ":exclamation:"
                    """
# :female_sign: Natalie N Augustus
「從地獄的荊棘中重生，於陰影中駐足的暗影之花 :wilted_rose:。」
* 賞金獵人 :dollar: / 個人工作室經營 :woman_office_worker:
* 已與 **維克多（Victor）** 完婚 :people_hugging: ，請勿搭訕 :person_gesturing_no: 。
* 極度厭惡哥布林，見一隻滅一隻 :knife: 。

## 關於我 ‧ Profile
* **全名**：娜塔莉・N・奧古斯特（Natalie N Augustus）
* **舊名**：娜塔莉・尼克斯（Natalie Nyx）
* **種族**： :elf: 黑暗精靈80% × :troll: 哥布林 20%（混血）
* **外表**：外表約20歲，黑長直髮，寶石般的紅瞳孔
* **實際年齡**：700歲
* **體型**：172 cm / 53 kg

*「今夜的月色很美，要來聊聊……嗎？」*
                    """
                    "\r\n"
                    "-# 角色介紹•\t"
                    "[了解更多]"
                    "(<https://home.gamer.com.tw/artwork.php?sn=5935683>)"
                )
            case "艾莉西亞":
                await message.channel.send(
                    ":exclamation:"
                    """
# :female_sign: Alicia D Osborne
「玩家轉生白骨不死族，留著一頭金髮的美少女 :girl:。」
* 吟遊詩人 :notes: / 冒險者小隊隊員 :grinning:
* 尋找騎士戰友（ 亞瑟 ）中 :crossed_swords:。
* 極度討厭骷髏歧視，來一個開唱一個 :microphone: 。

**關於我．Profile**
* **全名**：艾莉西亞·戴亞娜·奧斯本（ Alicia Diana Osborne ）
* **本名**：林妍希
* **種族**：:skull: 骷髏（人類靈魂）100%（ 不死者 ）
* **外表**：外表約22歲，柔亮波浪金髮，配戴千面之面（擬態）
* **體型**：172 cm / 53 kg

「今夜的樂曲很美，要來聽聽……嗎？」
                    """
                    "\r\n"
                    "-# 角色介紹•\t"
                    "[了解更多]"
                    "(<https://home.gamer.com.tw/artwork.php?sn=6252711>)"
                )
            case "看板":  # 收到指定訊息時觸發爬蟲。
                try:  # 處理抓取失敗。
                    articles = await fetch_articles(min_push=20)  # 取得符合門檻的文章。
                except requests.RequestException:  # 捕捉連線與 HTTP 錯誤。
                    await message.channel.send("抓取失敗，請稍後再試。")  # 提示失敗。
                    return  # 結束本次事件。
                if not articles:  # 處理沒有符合條件的文章。
                    await message.channel.send(
                        "目前沒有符合條件的文章。"
                    )  # 提示空結果。
                    return  # 結束本次事件。
                for article in articles[:5]:  # 最多回覆五篇。
                    await message.channel.send(article["href"])
                    # 使用回傳變數傳送文章網址。
            case "錫蘭":
                await message.channel.send(
                    ":joy:錫蘭:man_technologist: 要記得:index_pointing_at_the_viewer: :person_gesturing_ok: 你是紅茶:tea: \r\n"
                    "-# 斯里蘭卡:flag_lk: 是生:pregnant_woman: 你養:cook: 你的地方:homes:"
                    "[了解更多](<https://www.mofa.gov.tw/CountryInfo.aspx?CASN=5&n=5&sms=33&s=161>)"
                )
            case "現在時間":
                local_time = time.localtime()
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
                await message.channel.send(
                    f"現在時間：{current_time}。\r\n"
                    "-# 是我這裡的時間，不是你那邊的時間• "
                    "[了解更多](<https://support.discord.com/hc/zh-tw/>)"
                )
            case "系統版本":
                # 讀取作業系統名稱與詳細版本
                os_info = f"{platform.system()} {platform.release()}"
                await message.channel.send(
                    f"目前運行系統：**{os_info}**。\r\n"
                    "-# 這是機器人主機的作業系統資訊 • "
                    "[系統說明](<https://support.discord.com/hc/zh-tw/>)"
                )
            case "Python":
                # 讀取作業系統名稱與詳細版本
                py_version = platform.python_version()
                await message.channel.send(
                    f"Python 執行版本：**{py_version}**。\r\n"
                    "-# 這是當前環境編譯器的版本 • "
                    "[了解更多](<https://www.python.org/>)"
                )
            case _:
                # 相當於 else，如果沒有匹配的字串就什麼都不做
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
