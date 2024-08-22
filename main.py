import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
from youtube_dl import YoutubeDL
import asyncio
from youtubesearchpython import VideosSearch
from ast import alias


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=',', intents=discord.Intents.all()) 

@client.event
async def on_ready():
    print("The bot is ready to use.")
    print("________________________")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, i kill niggers!")

@client.command()
async def niggers(ctx):
    await ctx.send("did you know black people cause 54 percent of rapes?")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1275670027437342741)
    await channel.send("whats up nigger, welcome to the chudverse")


@client.event
async def on_member_join(member):
    channel = client.get_channel(1275670027437342741)
    await channel.send("Goodbyefaggot.")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    else:
        await ctx.send("nigger")


@client.command(pass_context = True)
async def quit(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("left successfully")
    else:
        await ctx.send("but im not in vc retard..")




client.run('MTI3NjA0Mzg2MjExMjA3NTc4Nw.GpJtrl.lxBWI5BLfk4wiNkNJlFa_v9IqUkKSKLLxpjBkY')