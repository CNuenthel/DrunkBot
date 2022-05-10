from discord.ext import commands
import datetime as dt
import json
import discord

class VolleyballDates:
    def __init__(self):
        self.dates: dict = {}
        self.load_dates()
        
    def load_dates(self):
        with open("22_VB_sched.json", "r") as f:
            data = json.load(f)

        for item in data:
            line = data[item]
            date = data[item]["date"]
            time = data[item]["time"]
            time_h = data[item]["time"][0]
            time_m = data[item]["time"][1]
            
            key = dt.datetime(date[0], date[1], date[2], time_h, time_m)
            self.dates[key] = {
                "time": time,
                "court": line["court"],
                "opp": line["opp"]
            }
            
    def add_date(self, year: int, month: int, day: int, hour: int, min: int, court: str, opposing_team: str):
        self.dates[dt.datetime(year, month, day, hour, min)] = {
            "time": [hour, min],
            "court": court.title(),
            "opp": opposing_team.title()
        }
        return self.dates[dt.datetime(year, month, day, hour, min)]

    def remove_date(self, year: int, month: int, day: int):
        removal = self.dates[dt.date(year, month, day)]
        self.dates.pop(dt.date(year, month, day))
        return removal

    def get_all_dates(self):
        return self.dates

    def get_next_date(self):
        for item in self.dates:
            if item > dt.datetime.now():
                return item, self.dates[item]
                break


class Volleycog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vb_dates = VolleyballDates()

    @commands.Cog.listener()
    async def on_ready(self):
        print("VolleyCog is Ready!")

    @commands.command()
    async def volleyball(self, ctx):
        date, match = self.vb_dates.get_next_date()
        embed=discord.Embed(
            title="Next Match", 
            description=f"{date.month}-{date.day}\nTime: {date.time()}\nCourt: {match['court']}\nAgainst: {match['opp']}\n", 
            color=discord.Color.blurple())
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Volleycog(bot))