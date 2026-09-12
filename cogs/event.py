import discord
from discord.ext import commands


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
                    "Hello, world!\r\n-# 我沒有日本駕照，所以我不會開/騎車•"
                    "[了解更多](https://support.discord.com/hc/zh-tw/)"
                )
            case "地震":
                await message.channel.send(
                    "-# 由於均均總是跌倒造成臺灣地震，已遭中華民國官方永久驅逐出境•\t"
                    "[了解更多](https://support.discord.com/hc/zh-tw/)"
                )
            case "Python":
                await message.channel.send(
                    ":desktop:"
                    """```py
import math

# 定義一個計算圓面積的函式
def calculate_area(radius):
    return math.pi * (radius ** 2)

# 設定半徑並呼叫函式
radius = 5
area = calculate_area(radius)

# 印出結果
print(f"當半徑為 {radius} 時，圓形的面積為: {area:.2f}")
                    ```"""
                    "\r\n"
                    "-# 這不是我寫的•\t"
                    "[了解更多](https://support.discord.com/hc/zh-tw/)"
                )
            case "SQL":
                await message.channel.send(
                    ":desktop:"
                    """```sql
SELECT * FROM dept       --department
SELECT * FROM emp       --employee
SELECT * FROM overtime
                    ```"""
                    "\r\n"
                    "-# 這不是我寫的•\t"
                    "[了解更多](https://support.discord.com/hc/zh-tw/)"
                )
            case _:
                # 相當於 else，如果沒有匹配的字串就什麼都不做
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
