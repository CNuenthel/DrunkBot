import json
from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.members = True

# Bot instance
bot = commands.Bot(command_prefix='.', intents=intents)

with open("config.json", "r") as f:
    config = json.load(f)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        
bot.run(config["token"])
