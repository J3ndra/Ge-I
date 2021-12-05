from discord.ext import commands
import discord
import requests
import json
import datetime

class weaponCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def weapons(self, ctx):
        ids = ctx.message.content.split()

        if len(ids) == 2:
            query = ids[-1].lower()
            url = f'https://api.genshin.dev/weapons/{query}'
            # urlPhoto = f'https://api.genshin.dev/weapons/{query}/portrait'
            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.blue(), title=f"{data.get('name', 'Could not get name.')}")
                embed.add_field(name="Type", value=f"{data.get('type', 'Could not get type.')}", inline=False)
                embed.add_field(name="Base Attack", value=f"**{data.get('baseAttack', 'Could not get base attack.')}**", inline=False)
                embed.add_field(name="Sub Stat", value=f"{data.get('subStat', 'Could not get sub stat.')}", inline=False)
                embed.add_field(name="Passive Name", value=f"{data.get('passiveName', 'Could not get passive name.')}", inline=False)
                embed.add_field(name="Passive Description", value=f"{data.get('passiveDesc', 'Could not get passive description.')}", inline=False)
                embed.add_field(name="Location", value=f"{data.get('location', 'Could not get location.')}", inline=False)
                embed.set_author(name=f"⭐ {data.get('rarity', 'Could not get id.')}", icon_url=url+'/icon')
                embed.set_image(url=url+'/icon')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

        else:
            url = 'https://api.genshin.dev/weapons'

            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.green(), title=f"Genshin Impact weapon list.", description='\n'.join(data))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)   


def setup(bot):
    bot.add_cog(weaponCog(bot))