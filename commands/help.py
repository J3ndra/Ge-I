from discord import embeds
from discord.ext import commands
import datetime
import discord

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(title="Ge-I", description="All available command for this bot.", color=discord.Color.blue())
        embed.set_thumbnail(url="https://i.ibb.co/DbNwVPJ/12342351-1per1.jpg")
        embed.add_field(name="*help", value="To show this message.", inline=False)
        embed.add_field(name="*ping", value="To show bot latency to this server", inline=False)
        embed.add_field(name="*weapons", value="To show all weapon in Genshin Impact. To show weapon details, `*weapons wolf-s-gravestone`.", inline=False)
        embed.add_field(name="*enemies", value="To show all enemy in Genshin Impact. To show enemy details, `*enemies abyss-mage`.", inline=False)
        embed.add_field(name="*artifacts", value="To show all artifact in Genshin Impact. To show artifact details, `*artifacts viridescent-venerer`.", inline=False)
        embed.add_field(name="*register UID", value="To register your Genshin Impact UID.", inline=False)
        embed.add_field(name="*getUid", value="Get your registered Genshin Impact UID.", inline=False)
        embed.add_field(name="*travNot", value="Get your travel Note such as Resin & Expedition", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(helpCog(bot))