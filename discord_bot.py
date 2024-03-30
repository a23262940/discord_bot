import discord
from discord.ext import commands
import os
from json import load
import asyncio

# 讀取設定檔
jsonFile = open('setData.json', 'r', encoding='UTF-8')
data = load(jsonFile)

# intents是要求機器人的權限
intents = discord.Intents.all()

# 機器人的指令前墜  command_prefix是前綴符號,可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    # 機器人上線預計執行的程式
    print(f'目前登入的身分:{bot.user}')

    # 更改機器人目前在玩的遊戲
    game = discord.Game('查看指令請用 "!botHelp"')
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.command()
async def load(ctx, extension):
    # 載入指令程式檔案
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"已將 {extension} 載入完成")


@bot.command()
async def unload(ctx, extension):
    # 卸載指令檔案
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"已將 {extension} 卸載完成")


@bot.command()
async def reload(ctx, extension):
    # 重新載指令檔案
    await bot.reload_extension(f"music.{extension}")
    await ctx.send(f"已將 {extension} 重新載入完成")


async def load_extensions():
    # 一開始BOT開機需要載入的檔案
    for filename in os.listdir("./channel"):
        if filename.endswith(".py"):
            await bot.load_extension(f"channel.{filename[:-3]}")

    for filename in os.listdir("./music"):
        if filename.endswith(".py"):
            await bot.load_extension(f"music.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(data['bot_token'])


if __name__ == '__main__':
    asyncio.run(main())
