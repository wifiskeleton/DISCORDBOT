import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import yt_dlp
import os
import time


bot = discord.ext.commands.Bot(command_prefix = ',', intents=discord.Intents.all())
client = commands.Bot(command_prefix=',', intents=discord.Intents.all()) 


@client.event
async def on_member_join(member):
    channel = client.get_channel(1275670027437342741)
    await channel.send("whats up nigger, welcome to the chudverse")


#musicbotcog

COG_FOLER_DIC = './cogs' 



@bot.event
async def on_ready():
    for file in os.listdir(COG_FOLER_DIC):
        if file.endswith('.py'):
            print(f'File found: {file}')
            if not COG_FOLER_DIC.startswith('./'):
                raise Exception('Cog folder must start with a dot and a slash!')
            shortend_dic = COG_FOLER_DIC[2:]
            await bot.load_extension(f'{shortend_dic}.{file[:-3]}')
            print(f'Loaded cog: {file[:-3]}')
bot.run('MTI3NjA0Mzg2MjExMjA3NTc4Nw.GpJtrl.lxBWI5BLfk4wiNkNJlFa_v9IqUkKSKLLxpjBkY')