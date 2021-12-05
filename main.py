import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')

# Running the bot
bot.run(BOT_TOKEN)