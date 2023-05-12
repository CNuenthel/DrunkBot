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


with open("data/volleyball_data_2023.json", "r") as f:
    data = json.load(f)

for item in data:
    line = data[item]
    line_date = [int(value) for value in line["date"]]
    VB_DATES.append(VBModel(dt.date(line_date[0], line_date[1], line_date[2]), line["court"], line["time"], line["team"]))
