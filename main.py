import sys
import asyncio
import discord
from discord.ext import commands
import os
import redis
from dotenv import load_dotenv
import config
import cashews
from cashews import Cache
from discord import Member
from discord.ext.commands import CommandNotFound
from discord.ext.commands import has_permissions, MissingPermissions
import google.generativeai as genai

genai.configure(api_key="AIzaSyDN7-LYxbUiMpca3PBUkgFhvk01GBw5o-0")

model = genai.GenerativeModel('gemini-pro')
# Loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize bot with commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix=',', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    
    extensions = ['cogs.MUSIC', 'cogs.Blacktea']
    for extension in extensions:
        try:
            await client.load_extension(extension)  # Use await here
            print(f'Successfully loaded {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}. Error: {e}')

@client.command(name = "askai")
async def askai(ctx: commands.Context, *, prompt: str):
    response = model.generate_context(prompt)

    await ctx.reply(response.txt)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason = reason)
    await ctx.send(f'User {member} has been booted from da chudverse nga.')

@kick.error
async def kick_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send ("nga u not even admin.")

@client.command()
@has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been booted from da chudverse nga.')

@ban.error
async def ban_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send ("nga u not even admin.")


@client.event
async def on_member_join(member):
    channel = client.get_channel(1275670027437342741)  # channel id
    if channel:
        await channel.send(f"Welcome to the chudverse, {member.mention}.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
# Run the client
client.run('MTI3NjA0Mzg2MjExMjA3NTc4Nw.GpJtrl.lxBWI5BLfk4wiNkNJlFa_v9IqUkKSKLLxpjBkY')
