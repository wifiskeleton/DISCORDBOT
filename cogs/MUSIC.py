import discord
import yt_dlp
from discord.ext import commands

class music(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.author.voice.channel if ctx.author.voice else None
        if not vc:
            return await ctx.send("You're not connected to a voice channel!")
        if not ctx.voice_client:
            await vc.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if info and 'entries' in info and len(info['entries']) > 0:
                    info = info['entries'][0]
                    url = info['url']
                    title = info['title']
                    self.queue.append((url, title))
                    await ctx.send(f"Added to queue: **{title}**")
                else:
                    await ctx.send("No results found for your search.")
        
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        FFMPEG_OPTIONS = {'options': '-vn'}
        if self.queue:
            url, title = self.queue.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(
                url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source,
                                  after=lambda _: self.client.loop.create_task(
                                      self.play_next(ctx)))
            await ctx.send(f"Now playing: **{title}**")
        elif not ctx.voice_client.is_playing():
            await ctx.send("Queue is empty!")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song!")
        else:
            await ctx.send("I'm not currently playing any music.")

    @commands.command(name="pause")
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.voice_client.pause()
            await ctx.send("Paused the music.")
        else:
            await ctx.send("I'm not currently playing any music.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
            await ctx.send("Resumed the music.")
        else:
            await ctx.send("The music is not paused.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(music(client))
