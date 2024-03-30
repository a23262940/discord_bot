import discord
from discord.ext import commands
import os
import asyncio

# 音樂清單
play_list = []

# 定義名稱為Main的cog
class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str = ""):
        # 撥放音樂
        # 判斷機器人是否在頻道
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels)
            await voiceChannel.connect()
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # 判斷是否為加入清單
        if voice.is_playing():
            play_list.append(url)
            await ctx.send("已加入等待列表")
        else:
            # 判斷音樂檔是否存在
            song_exist = os.path.isfile('song.mp3')
            try:
                if song_exist:
                    os.remove("song.mp3")
            except PermissionError:
                await ctx.send("等待目前的音樂結束或停止")
                return

            # 將檔案變mp3
            os.system(f"D:/python/api/discord_bot/music/yt-dlp_x86.exe --extract-audio --audio-format mp3 --audio-quality 0 {url}")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe',
                                              source="song.mp3"), after=lambda x: self.endSong("D:/python/api/discord_bot/song.mp3"))
            await ctx.send("播放中")

    def endSong(self, path):
        # 播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
        os.remove(path)
        if len(path) != 0:
            try:
                voice = discord.utils.get(self.bot.voice_clients)
                url = play_list.pop(0)
                os.system(
                    f"D:/python/api/discord_bot/music/yt-dlp_x86.exe --extract-audio --audio-format mp3 --audio-quality 0 {url}")
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",
                                                  source="song.mp3"), after=lambda x: self.endSong("D:/python/api/discord_bot/song.mp3"))
            except:
                print("end")
    
    @commands.command()
    async def skip(self, ctx):
        # 跳過音樂
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await self.play_next(ctx)
            await ctx.send("已成功跳過")
        else:
            await ctx.send("當前沒有音樂正在播放")

    async def play_next(self, ctx):
        song_path = 'D:\\python\\api\\discord_bot\\song.mp3'
        if len(play_list) > 0:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            next_song = play_list.pop(0)  # 从队列中移除并获取下一首曲目
            print(next_song)
            os.system(
                    f"D:/python/api/discord_bot/music/yt-dlp_x86.exe --extract-audio --audio-format mp3 --audio-quality 0 {next_song}")
            if os.path.exists(song_path):
                try:
                    os.remove(song_path)
                except Exception as e:
                    await ctx.send(f"發生異常 錯誤碼:{e}")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",
                                                  source="song.mp3"), after=lambda x: self.endSong("D:/python/api/discord_bot/song.mp3"))

# Cog 載入Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
