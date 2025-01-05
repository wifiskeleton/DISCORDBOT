import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been booted from da chudverse.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned from da chudverse.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        """Mute a user by adding the 'Muted' role."""
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            await ctx.send("Muted role not found, please make sure the bot created it on first join.")
            return

        # Check if the user is already muted
        if muted_role in member.roles:
            await ctx.send(f"{member.mention} is already muted.")
            return

        # Add the muted role to the user without modifying other roles
        await member.add_roles(muted_role, reason=f"Muted by {ctx.author}")
        
        # Send a confirmation message
        await ctx.send(f"{member.mention} has been muted.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a user by removing the 'Muted' role."""
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            await ctx.send("Muted role not found, please make sure the bot created it on first join.")
            return

        # Check if the user is muted
        if muted_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return

        # Remove the muted role from the user without modifying other roles
        await member.remove_roles(muted_role, reason=f"Unmuted by {ctx.author}")

        # Send a confirmation message
        await ctx.send(f"{member.mention} has been unmuted.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
