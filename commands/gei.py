from discord import embeds
from discord.ext import commands
import datetime
import discord

class geiCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def gei(self, ctx):
        embed=discord.Embed(title="Ge-I Discord Bot", description="Fan-made Genshin Impact Bot for Discord", color=0x82cbec)
        embed.set_author(name="Koh", url="https://github.com/J3ndra/Ge-I", icon_url="https://avatars.githubusercontent.com/u/32166625?v=4")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/32166625?v=4")
        embed.add_field(name="Github", value="https://github.com/J3ndra/Ge-I", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(geiCog(bot))