import json
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# GET PREFIXES
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')
    print('-------')
    print('Joined Guild:')
    for guild in bot.guilds:
        print(f'{guild.name} - {guild.id}')

# Bot joining a new server
@bot.event
async def on_guild_join(guild):
    print(f"{bot.user.name} joined {guild.name} - {guild.id}.")
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '*'

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4) 

#Bot leaving a server
@bot.event
async def on_guild_remove(guild):
    print(f"{bot.user.name} has been kicked from {guild.name} - {guild.id}.")
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Bot change prefix with permission
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed = discord.Embed(color = 0xff5900, title="Prefix changed!", description=f"New prefix : `{prefix}`.")
    await ctx.send(embed=embed)

# Read all command on 'commands' folder
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

    else:
        print(f'Unable to load {filename[:-3]}')

# Running the bot
bot.run(BOT_TOKEN)