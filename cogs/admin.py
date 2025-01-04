import discord
from discord.ext import commands
import asyncio

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
    async def mute(self, ctx, member: discord.Member, duration: str = None):
        """Mute a user indefinitely or for a specified duration, and remove their 'cool' role."""
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        cool_role = discord.utils.get(guild.roles, name="cool")  # Lowercase 'cool' role

        if not muted_role:
            await ctx.send("Muted role not found, please make sure the bot created it on first join.")
            return

        # Check if the user is already muted
        if muted_role in member.roles:
            await ctx.send(f"{member.mention} is already muted.")
            return

        # Add the muted role to the user
        await member.add_roles(muted_role, reason=f"Muted by {ctx.author}")

        # Remove the 'cool' role if they have it
        if cool_role in member.roles:
            await member.remove_roles(cool_role, reason="Removed during mute")

        # Deny the muted user access to all channels
        for channel in guild.text_channels:
            await channel.set_permissions(muted_role, read_messages=False)

        # Send the mute message only once
        mute_message = f"{member.mention} has been muted and the 'cool' role has been removed."
        
        # If there is a duration, handle it after the message
        if duration:
            try:
                time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
                unit = duration[-1].lower()
                if unit not in time_units:
                    raise ValueError("Invalid time unit. Use s, m, h, or d.")
                
                time_amount = int(duration[:-1])
                total_seconds = time_amount * time_units[unit]
                await asyncio.sleep(total_seconds)

                # Remove the muted role and restore channel permissions
                await member.remove_roles(muted_role, reason="Mute duration expired")
                for channel in guild.text_channels:
                    await channel.set_permissions(muted_role, read_messages=None)  # Restore default permissions

                # Optionally, add the 'cool' role back if it was removed during mute
                if cool_role and cool_role not in member.roles:
                    await member.add_roles(cool_role, reason="Restored after unmute")

                mute_message = f"{member.mention} has been unmuted nigga."

            except ValueError:
                await ctx.send("Invalid duration format. Use a number followed by s, m, h, or d (e.g., 10m).")
                return

        await ctx.send(mute_message)  # Send the mute/unmute message once

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a user."""
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            await ctx.send("Muted role not found, please make sure the bot created it on first join.")
            return

        if muted_role in member.roles:
            await member.remove_roles(muted_role, reason=f"Unmuted by {ctx.author}")
            await ctx.send(f"{member.mention} has been unmuted!")
        else:
            await ctx.send(f"{member.mention} is not muted.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
