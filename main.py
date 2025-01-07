import sys
import asyncio
import discord
from neuralintents import GenericAssistant
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

# Initialize bot with commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix=',', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    
    extensions = ['cogs.MUSIC', 'cogs.Blacktea', 'cogs.admin']
    for extension in extensions:
        try:
            await client.load_extension(extension)  # Use await here
            print(f'Successfully loaded {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}. Error: {e}')

@client.event
async def on_guild_join(guild):
    """Create the 'Muted' role when the bot first joins a server."""
    muted_role = discord.utils.get(guild.roles, name="Muted")
    
    # Create the muted role if it doesn't exist
    if not muted_role:
        muted_role = await guild.create_role(
            name="Muted",
            permissions=discord.Permissions(send_messages=False, speak=False)
        )
        # Set permissions for all channels to mute users with this role
        for channel in guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)
        
        print(f"Muted role created in {guild.name}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# Run the client
client.run('MTMyMjc1MDc5ODU1OTcxMTMwNA.Gg0Ly-._iuGySahDsvXxINLMxRlu8QNtfaKOSTTv8EJko')
