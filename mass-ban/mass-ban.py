import datetime
import typing

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class MassBan(commands.Cog): 
    """Author: @dpsKita"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mban"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def massban(self, ctx, members: commands.Greedy[discord.Member], days: typing.Optional[int] = 0, *, reason: str = None):
        """*Mass-bans members*\n
        Note(s)
        ├─ `Members` - seperate by space.
        ├─ `Days` - deleted messages for number of days (optional; default is 0).
        └─ `Reason` - self explanatory; optional."""

        if members is not None:
            for member in members:
                try:
                    await member.ban(delete_message_days=days, reason=f"{reason if reason else None}")
                    embed = discord.Embed(color=0x2f3136, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    
                    embed.add_field(name="Banned user(s)", value=f"{members.mention} | ID: {members.id}", inline=False)
                    embed.add_field(name="Banned by:", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
                    embed.add_field(name="Reason", value=reason, inline=False)

                    await ctx.send(embed=embed)
                except discord.Forbidden:
                    await ctx.send("I don't have the proper permissions to ban people.")
                except Exception as e:
                    await ctx.send("An unexpected error occurred, please check the logs for more details.")
                    return
        elif members is None:
            return await ctx.send_help(ctx.command)
                        
def setup(bot):
    bot.add_cog(MassBan(bot))