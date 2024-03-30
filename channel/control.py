import discord
from discord.ext import commands

from json import load

# 讀取設定檔
jsonFile = open('setData.json', 'r', encoding='UTF-8')
data = load(jsonFile)

# 定義名稱為Main的cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # 检查用户是否在语音频道中
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send("您必須先加入一個頻道。")
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if ctx.author.voice == None:
            await ctx.send("You are not connected to any voice channel")
        elif voice == None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Already connected to a voice channel")


    @commands.command()
    async def leave(self, ctx: commands.context):
        # 離開call他那個伺服器的所在頻道
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await ctx.send("機器人未連接到語音通道")
        else:
            await voice.disconnect()

    @commands.command()
    async def shutdown(self, ctx):
        # 關閉機器人
        # 檢查指令發送是否為機器人擁有者
        if str(ctx.author.id) == data['user_id']:
            await ctx.send("關閉中...")
            await self.bot.close()
        else:
            await ctx.send("你沒有權限")

    @commands.command()
    async def botHelp(self, ctx):
        # 查看指令
        # 開啟指令的文字檔來使用指令
        strings = ''
        for line in data['instructions']:
            strings += line['instruction']
        await ctx.send(strings)

# Cog 載入Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
