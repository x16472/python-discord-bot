import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv  # 1. 引入套件

load_dotenv()
token = os.getenv("DCToken")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)
cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
# 模組統一由load_extensions()非同步載入。


@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    if not os.path.exists(cogs_dir):
        print(f"警告：找不到資料夾 {cogs_dir}，請確認是否存在。")
        return
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"已成功載入模組：{filename}")


async def main():
    async with bot:
        await load_extensions()
        # 請確保您已將 DCToken 設定在環境變數中，或直接在此處填入字串
        if not token:
            print("錯誤：找不到環境變數 DCToken，請確認是否已設定。")
            return
        await bot.start(token)


# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
