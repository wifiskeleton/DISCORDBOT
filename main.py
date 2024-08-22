import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ',')

@client.event
async def on_ready():
    print("The bot is ready to use.")
    print("________________________")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, i kill niggers!")


client.run('MTI3NjA0Mzg2MjExMjA3NTc4Nw.GpJtrl.lxBWI5BLfk4wiNkNJlFa_v9IqUkKSKLLxpjBkY')