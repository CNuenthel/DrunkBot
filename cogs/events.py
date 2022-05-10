
from discord.ext import commands
import discord

class Events(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("MyClientCog is Ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "terry" in message.content.lower():
            await message.channel.send("Oh you mean Tatters?")

        if message.content.lower() == "good morning kanye":
            await message.channel.send("Shut the fuck up.")

        if message.content.lower() == "bruh":
            await message.channel.send("Bruh...")

def setup(bot):
    bot.add_cog(Events(bot))

