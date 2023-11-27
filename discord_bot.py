import discord
from discord.ext import commands
import os
from json import load

#讀取設定檔
jsonFile = open('setData.json','r',encoding='UTF-8')
data = load(jsonFile)

#intents是要求機器人的權限
intents = discord.Intents.all()

#機器人的指令前墜  command_prefix是前綴符號,可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix='!',intents=intents)

#音樂清單
play_list = []

@bot.event
async def on_ready():
    #機器人上線預計執行的程式
    print(f'目前登入的身分:{bot.user}')
    
    #更改機器人目前在玩的遊戲
    game = discord.Game('查看指令請用 "!botHelp"')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    
@bot.command()
async def join(ctx):
    #這裡的指令會讓機器人進入call他的頻道
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.send("機器人未連接到語音通道")
    elif voice == None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    else:
        await ctx.send("已連接成功")
        
@bot.command()
async def leave(ctx):
    #離開call他那個伺服器的所在頻道
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("機器人未連接到語音通道")
    else:
        await voice.disconnect()
        
@bot.command()
async def shutdown(ctx):
    #關閉機器人
    #檢查指令發送是否為機器人擁有者
    if str(ctx.author.id) == data['user_id']:
        await ctx.send("關閉中...")
        await bot.close()
    else:
        await ctx.send("你沒有權限")
        
@bot.command()
async def botHelp(ctx):
    #查看指令
    #開啟指令的文字檔來使用指令
    strings = ''
    for line in data['instructions']:
        strings += line['instruction']
    await ctx.send(strings)

@bot.command()
async def play(ctx,url :str = ""):
    #撥放音樂
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #判斷機器人是否在頻道
    if voice is None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    #判斷是否為加入清單
    if voice.is_playing():
        play_list.append(url)
        await ctx.send("已加入等待列表")
    else:
        #判斷音樂檔是否存在
        song_exist = os.path.isfile('song.mp3')
        try:
            if song_exist:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("等待目前的音樂結束或停止")
            return
        
        #將檔案變mp3
        os.system(f"yt-dlp_x86.exe --extract-audio --audio-format mp3 --audio-quality 0 {url}")
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio(executable = 'ffmpeg/bin/ffmpeg.exe', source = "song.mp3"), after = lambda x: endSong("song.mp3"))
        await ctx.send("播放中")


def endSong(path):
    #播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
    os.remove(path)
    if len(path) != 0:
        try:
            voice = discord.utils.get(bot.voice_clients)
            url = play_list[0]
            del play_list[0]
            os.system(f"yt-dlp_x86.exe --extract-audio --audio-format mp3 --audio-quality 0 {url}")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"song.mp3")
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp3"),after = lambda x: endSong("song.mp3"))
        except:
            print('end')
    

@bot.command()
async def resume(ctx):
    #繼續音樂
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('已繼續播放音樂')

@bot.command()
async def stop(ctx):
    #暫停音樂
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('已經暫停播放')
    
@bot.command()
async def skip(ctx):
    #跳過音樂
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

if __name__ == '__main__':
    bot.run(data['bot_token'])