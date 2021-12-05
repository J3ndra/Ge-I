from discord.ext import commands
import discord
import requests
import json
import datetime

class artifactsCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def artifacts(self, ctx):
        ids = ctx.message.content.split()

        if len(ids) == 2:
            query = ids[-1].lower()
            url = f'https://api.genshin.dev/artifacts/{query}'

            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.blue(), title=f"{data.get('name', 'Could not get name.')}")
                embed.add_field(name="2 Piece Bonus", value=f"{data.get('2-piece_bonus', 'Could not get 2 piece bonuses.')}", inline=False)
                embed.add_field(name="4 Piece Bonus", value=f"{data.get('4-piece_bonus', 'Could not get 4 piece bonuses.')}", inline=False)
                embed.set_author(name=f"⭐ {data.get('max_rarity', 'Could not get id.')}", icon_url=url+'/flower-of-life')
                embed.set_image(url=url+'/flower-of-life')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

        else:
            url = 'https://api.genshin.dev/artifacts'

            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.green(), title=f"Genshin Impact artifact list.", description='\n'.join(data))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)   

def setup(bot):
    bot.add_cog(artifactsCog(bot))