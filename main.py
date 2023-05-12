import json
from discord.ext import commands
import discord
import platform
from volleyball import VB_DATES
import datetime as dt


# Bot instance
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Read config file for bot
with open("config.json", "r") as f:
    config = json.load(f)

# On ready action
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print("Drunkbot Drunk and Ready for Drinking!")


# # Message event responses
# @bot.event
# async def on_message(message):
#     if "terry" in message.content.lower():
#         await message.channel.send("Oh you mean Tatters?")
#
#     if message.content.lower() == "good morning kanye":
#         await message.channel.send("Shut the fuck up.")
#
#     if message.content.lower() == "bruh":
#         await message.channel.send("Bruh...")


# ----------------------------------------------------------------------------------------------------------------------
# VOLLEYBALL COMMANDS

# Display volleyball game information from vb data
@bot.command(aliases=["vb"])
async def volleyball(ctx):
    today = dt.date(2023, 5, 22)#dt.date.today()
    print(today)
    closest_date = None
    closest_vb_date = None

    for vb_date in VB_DATES:
        compare_date = vb_date.date

        if compare_date < today:
            continue

        if closest_date is None or compare_date < closest_date:
            closest_date = compare_date
            closest_vb_date = vb_date

    embed = discord.Embed(
        title="Next Match",
        description=f"Date: {closest_vb_date.date}\n"
                    f"Time: {closest_vb_date.time} PM\n"
                    f"Court: {closest_vb_date.court}\n"
                    f"Against: {closest_vb_date.team}",
        color=discord.Color.blurple())
    embed.set_author(
        name="VolleyBot",
        icon_url="https://cdn-icons-png.flaticon.com/512/2761/2761875.png"),

    await ctx.send(embed=embed)

# Run bot
bot.run(config["token"])
