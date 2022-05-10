from discord.ext import commands
import discord

class General(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("GeneralCog is Ready!")

    @commands.command()
    async def send_pod(self, ctx):

        await ctx.send(
            f"Here you go!\n"
            f"Sam: https://drive.google.com/file/d/1aMA0phGVGz4jGJOQA1_MnXQR9nKWgDnp/view?usp=sharing\n"
            f"Cody: https://drive.google.com/file/d/1Udoa_wutaF40YwXCLe-aXOxHaP9XHNK0/view?usp=sharing"
        )
    
def setup(bot):
    bot.add_cog(General(bot))