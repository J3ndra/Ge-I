from discord.ext import commands
import discord
import datetime

class pingCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def ping(self, ctx):
        ping=round(self.bot.latency*1000)
        if ping<=100:
            embed = discord.Embed(title="Bot ping.", description=f"Bot latency to the server is `{ping} ms`", color=discord.Color.green())
        elif ping<=300:
            embed = discord.Embed(title="Bot ping.", description=f"Bot latency to the server is `{ping} ms`", color=discord.Color.orange())
        elif ping>301:
            embed = discord.Embed(title="Bot ping.", description=f"Bot latency to the server is `{ping} ms`", color=discord.Color.red())
        
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(pingCog(bot))