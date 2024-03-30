import discord
from discord.ext import commands

# 定義名稱為Main的cog
class Stop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def stop(self, ctx):
        # 暫停音樂
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('已經暫停播放')

# Cog 載入Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Stop(bot))
