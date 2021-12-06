import discord
from discord.ext import commands
from typing import Union
import json
from discord.ext.commands.errors import MissingRequiredArgument
import datetime

class regisCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    async def _user_uid(self, ctx: commands.Context, user: Union[discord.User, discord.Member, int, None]) -> int:
        """Helper function to either get the uid or raise an error"""
        if isinstance(user, int):
            return user

    @commands.command()
    async def register(self, ctx: commands.Context, user: int):
        uid = await self._user_uid(ctx, user)
        with open('uid.json', 'r') as f:
            geiUID = json.load(f)
        
        geiUID[str(ctx.message.author.id)] = uid

        with open('uid.json', 'w') as f:
            json.dump(geiUID, f, indent=4)

        embed = discord.Embed(title=f'{ctx.message.author.display_name} UID has been registered.', color=discord.Color.green())
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @register.error
    async def register_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title="Please insert your Genshin Impact UID.", description="Example, `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(regisCog(bot))