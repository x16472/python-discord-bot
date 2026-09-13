import time  # 引入時間模組，用來計算遊玩時間

import discord
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 在 Cog 裡面，使用 @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        # 這裡的 print 會在 main.py 時，跟著 main.py 的 on_ready 一起在終端機跳出來
        print(f"[{self.__class__.__name__}] 狀態模組已成功與 Discord 連線！")
        # 建立進階的遊戲活動狀態
        activity = discord.Activity(
            type=discord.ActivityType.playing,  # 狀態類型：正在玩
            name="Python",
            details="以後就會有了",
            state="正在學習中",  # 遊戲目前的階段 (第二行小字)
            # 設定開始時間，會在 Discord 畫面上顯示「已遊玩：XX 分鐘」
            timestamps={"start": int(time.time())},
            # 設定遊戲圖標
            # 裡面的代號需要到 Discord Developer Portal
            # 其中的Rich Presence->Art Assets上傳圖片並命名）
            assets={
                "large_image": "logo",  # 在後台設定的大圖代號
                "large_text": "League of Legends",  # 滑鼠移到大圖上顯示的文字
                "small_image": "rank_icon",  # 在後台設定的小圖代號（例如牌位）
                "small_text": "菁英",  # 滑鼠移到小圖上顯示的文字
            },
        )
        # 套用自訂狀態（注意：這裡要用 self.bot）
        await self.bot.change_presence(
            status=discord.Status.online,  # 在線(online)、閒置(idle)、請勿打擾(dnd)
            activity=activity,
        )


# 引入函數 main.py 呼叫 load_extension 時，會自動執行這個 setup 函式
async def setup(bot):
    await bot.add_cog(Stats(bot))
