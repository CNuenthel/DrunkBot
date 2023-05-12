from discord.ext import commands
import datetime as dt
import json
import discord

VB_DATES = []


class VBModel:
    def __init__(self, date, court, time, team):
        self.date = date
        self.court = court
        self.time = time
        self.team = team


with open("../volleyball_data_2023.json", "r") as f:
    data = json.load(f)

for item in data:
    line = data[item]
    line_date = [int(value) for value in line["date"]]
    VB_DATES.append(VBModel(dt.date(line_date[0], line_date[1], line_date[2]), line["court"], line["time"], line["team"]))


class Volleyball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vb_dates = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("VolleyBot is Ready!")

    @commands.command(aliases=["vb"])
    async def volleyball(self, ctx):
        today = dt.date.today()
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


def setup(bot):
    bot.add_cog(Volleyball(bot))
