import discord
from discord.ext import commands

# 定義名稱為Main的cog
class Resume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def resume(self, ctx):
        # 繼續音樂
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('已繼續播放音樂')

# Cog 載入Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Resume(bot))
