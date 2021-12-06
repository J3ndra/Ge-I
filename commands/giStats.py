from discord.colour import Color
from discord.ext import commands
import discord
import json
from discord.ext.commands import errors
import genshinstats as gs
from cachetools import TTLCache
from discord.ext.commands.errors import CommandInvokeError
import datetime

from genshinstats.errors import AccountNotFound

class giStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        gs.set_cookies_auto()
        self.cache = TTLCache(1024, 3600)
        gs.install_cache(self.cache)

    # Get UID
    async def _get_uid(self, ctx):
        with open('uid.json', 'r') as file:
            uid = json.load(file)
        return uid[str(ctx.message.author.id)]

    @commands.command()
    async def getUid(self, ctx):
        uid = await self._get_uid(ctx)
        embed = discord.Embed(title=f'Your UID is {uid}.',  description="This message will automatically deleted after 30 second.",color=discord.Color.green())
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed, delete_after=30.0)

    @getUid.error
    async def getUid_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command()
    async def travNot(self, ctx):
        uid = await self._get_uid(ctx)
        try:
            notes = gs.get_notes(uid)
            embed = discord.Embed(title=f'{ctx.message.author.display_name} Notes.', color=discord.Color.blue())
            embed.add_field(name="Current resin.", value=f"{notes['resin']}/{notes['max_resin']}")
            embed.add_field(name="Expeditions.", value=f"{len(notes['expeditions'])}/{notes['max_expeditions']}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        except gs.errors.DataNotPublic:
            embed = discord.Embed(title=f"Your account is not public.", description="Go to hoyolab to make your account public.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        except gs.errors.AccountNotFound:
            embed = discord.Embed(title=f"Your registered UID is invalid.", description="Example `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            

    @travNot.error
    async def travNot_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error
    

def setup(bot):
    bot.add_cog(giStatsCog(bot))