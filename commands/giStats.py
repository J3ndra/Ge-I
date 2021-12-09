import os
from discord.ext import commands
import discord
import json
import genshinstats as gs
from discord.ext.commands.errors import CommandInvokeError
import datetime
import re

character_icons = {
    "PlayerGirl": "Traveler",
    "PlayerBoy": "Traveler",
    "Ambor": "Amber",
    "Qin": "Jean",
    "Hutao": "Hu Tao",
    "Feiyan": "Yanfei",
    "Kazuha": "Kadehara Kazuha",
    "Sara": "Kujou Sara",
    "Shougun": "Raiden Shogun",
    "Tohma": "Thoma",
}

def _recognize_character_icon(url: str) -> str:
    """Recognizes a character's icon url and returns its name."""
    exp = r"game_record/genshin/character_.*_(\w+)(?:@\dx)?.png"
    match = re.search(exp, url)
    if match is None:
        raise ValueError(f"{url!r} is not a character icon or image url")
    character = match.group(1)
    return character_icons.get(character) or character

class giStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        gs.set_cookie(ltuid=os.getenv('ltuid'), ltoken=os.getenv('lttoken'))

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
            sec = int(notes['until_resin_limit'])
            toHours = str(datetime.timedelta(seconds=sec))
            embed.add_field(name="Expeditions.", value=f"{len(notes['expeditions'])}/{notes['max_expeditions']}.")
            embed.add_field(name="Boss Discount.", value=f"{notes['remaining_boss_discounts']}/{notes['max_boss_discounts']}")
            embed.add_field(name="Current resin.", value=f"{notes['resin']}/{notes['max_resin']}. Time until full {toHours}.", inline=False)
            if notes['claimed_commission_reward'] == False:
                msg = 'Commission rewards claimed'
            else:
                msg = 'Commission rewards not claimed'

            embed.add_field(name="Commissions", value=f"{notes['completed_commissions']}/{notes['total_commissions']}.\n{msg}.", inline=False)
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
        except gs.errors.GenshinStatsException:
            embed = discord.Embed(title=f"I'm sorry but `*travNot` currently under maintain.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    async def travChars(self, ctx):
        uid = await self._get_uid(ctx)
        list = []
        try:
            characters = gs.get_user_stats(uid)['characters']
            for char in characters:
                list.append(f"{char['rarity']}* {char['name']} ({char['level']}).")
            embed = discord.Embed(title=f'{ctx.message.author.display_name} Characters.', description=f'\n'.join(list),color=discord.Color.blue())
            embed.add_field(name="Total Characters", value=f"{len(list)}")
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

    @commands.command()
    async def travStats(self, ctx):
        uid = await self._get_uid(ctx)
        try:
            stats = gs.get_user_stats(uid)['stats']
            embed = discord.Embed(title=f"{ctx.message.author.display_name} Stats.", color=discord.Color.blue())
            for field, value in stats.items():
                embed.add_field(name=f"{field}", value=f"{value}")
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

    @commands.command()
    async def travAccount(self, ctx):
        uid = await self._get_uid(ctx)
        try:
            stats = gs.get_game_accounts(uid)
            embed = discord.Embed(title=f"{ctx.message.author.display_name} Genshin Impact account.", color=discord.Color.blue())
            embed.add_field(name="Server", value=f"{stats['server']}")
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
        except gs.errors.NotLoggedIn:
            embed = discord.Embed(title=f"I'm sorry but you need to be logged in to the game.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)


    

    @commands.command()
    async def travAbyss(self, ctx):
        uid = await self._get_uid(ctx)
        try:
            spiral_abyss = gs.get_spiral_abyss(uid)
            spiral = spiral_abyss
            embed = discord.Embed(title=f"{ctx.message.author.display_name} Abyss Stats Season {spiral['season']}.", color=discord.Color.blue())
            embed.add_field(name="Start Time.", value=f"{spiral['season_start_time']}")
            embed.add_field(name="End Time.", value=f"{spiral['season_end_time']}")
            embed.add_field(name="Stats.", value=f"\n".join(f"{field}: {value}" for field, value in spiral['stats'].items()), inline=False)
            embed.add_field(name=f"Most Played - {spiral['character_ranks']['most_played'][0]['value']} times.", value=f"{spiral['character_ranks']['most_played'][0]['name']} - {spiral['character_ranks']['most_played'][0]['rarity']}⭐")
            embed.add_field(name=f"Most Kills - {spiral['character_ranks']['most_kills'][0]['value']} kill.", value=f"{spiral['character_ranks']['most_kills'][0]['name']} - {spiral['character_ranks']['most_kills'][0]['rarity']}⭐")
            embed.add_field(name=f"Strongest Strike - {spiral['character_ranks']['strongest_strike'][0]['value']} in one shot.", value=f"{spiral['character_ranks']['strongest_strike'][0]['name']} - {spiral['character_ranks']['strongest_strike'][0]['rarity']}⭐")
            embed.add_field(name=f"Most Damage Taken - {spiral['character_ranks']['most_damage_taken'][0]['value']} in total.", value=f"{spiral['character_ranks']['most_damage_taken'][0]['name']} - {spiral['character_ranks']['most_damage_taken'][0]['rarity']}⭐")
            embed.add_field(name=f"Most Burst Used - {spiral['character_ranks']['most_bursts_used'][0]['value']} times.", value=f"{spiral['character_ranks']['most_bursts_used'][0]['name']} - {spiral['character_ranks']['most_bursts_used'][0]['rarity']}⭐")
            embed.add_field(name=f"Most Skills Used - {spiral['character_ranks']['most_skills_used'][0]['value']} times.", value=f"{spiral['character_ranks']['most_skills_used'][0]['name']} - {spiral['character_ranks']['most_skills_used'][0]['rarity']}⭐")
            # for field, value in spiral['floors'][0]['chambers'][].items():
            #     print(f"{field}: {value}")
            # embed.add_field(name=f"Chambers Record.", value=f"\n".join())
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


#   ALL ERROR HANDLING FOR COMMANDS ABOVE
    @travNot.error
    async def travNot_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error

    @travStats.error
    async def travStats_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error

    @travAbyss.error
    async def travAbyss_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error
        
    @travChars.error
    async def travChars_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(title="Could not find your UID, please register your UID using `*register UID`.", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(giStatsCog(bot))