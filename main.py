import json
from discord.ext import commands
import discord
import os
import pretty_help

intents = discord.Intents.default()
intents.members = True

# Bot instance
bot = commands.Bot(command_prefix='.', intents=intents, help_command=pretty_help.PrettyHelp())

with open("config.json", "r") as f:
    config = json.load(f)


@bot.command()
async def load(ctx, extension):
    """ Loads a cog """
    try:
        bot.load_extension(f"cogs.{extension.lower()}")
        await ctx.send(f"{extension} has been loaded! 😌")
    except commands.errors.ExtensionNotFound:
        await ctx.send(f"{extension} was not found as an available cog. 🤔")


@bot.command()
async def unload(ctx, extension):
    """ Unloads a cog """
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} has been removed 😌")
    except commands.errors.ExtensionNotFound:
        await ctx.send(f"{extension} was not found as a current cog. 🤔")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        
bot.run(config["token"])
