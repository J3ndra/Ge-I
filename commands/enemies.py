from discord.ext import commands
import discord
import requests
import json
import datetime

class enemiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def enemies(self, ctx):
        ids = ctx.message.content.split()

        if len(ids) == 2:
            query = ids[-1].lower()
            url = f'https://api.genshin.dev/enemies/{query}'
            urlPhoto = f'https://api.genshin.dev/enemies/{query}/portrait'
            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.blue(), title=f"{data.get('name', 'Could not get name.')}", description=f"{data.get('description', 'Could not get description.')}")
                embed.set_author(name=f"{data.get('id', 'Could not get id.')}", icon_url=url+'/icon')
                embed.add_field(name="Region", value=f"{data.get('region', 'Could not get region.')}", inline=False)
                embed.add_field(name="Type", value=f"{data.get('type', 'Could not get type.')}", inline=False)
                embed.add_field(name="Family", value=f"{data.get('family', 'Could not get family.')}", inline=False)
                embed.add_field(name="Faction", value=f"{data.get('faction', 'Could not get faction.')}", inline=False)
                if(len(data['elements'])) > 0:
                    elements = ', '.join(data.get('elements', '0'))
                    embed.add_field(name="Elements", value=elements, inline=False)

                if (len(data.get('drops', '')) > 0):
                    drops = data.get('drops')
                    embed.add_field(name="Drops.", value=f"\n".join(f"{drop['name']} | {drop['rarity']}⭐ | Minimum level {drop['minimum-level']}" for drop in drops), inline=False)
                else:
                    pass

                if (len(data.get('artifacts', '')) > 0):
                    artifacts = data.get('artifacts')
                    embed.add_field(name="Drops.", value=f"\n".join(f"{artifact['name']} ({artifact['set']}) | {artifact['rarity']}⭐" for artifact in artifacts), inline=False)
                else:
                    pass

                if (len(data.get('elemental-description', '')) > 0):
                    elementalDescription = data.get('elemental-description')
                    for i in elementalDescription:
                        embed.add_field(name=f"{i['element']}", value=f"{i['description']}")
                else:
                    pass

                embed.add_field(name="Mora Gained", value=f"{data.get('mora-gained', 'Could not get mora gained.')}", inline=False)
                embed.set_image(url=urlPhoto)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

        else:
            url = 'https://api.genshin.dev/enemies'
            
            try:
                resp = requests.get(url=url)
                data = json.loads(resp.content)
                embed = discord.Embed(color = discord.Color.green(), title=f"Genshin Impact enemy list.", description='\n'.join(data))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(color = discord.Color.red(), title="Something went wrong.", description="Please try again later.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(enemiesCog(bot))