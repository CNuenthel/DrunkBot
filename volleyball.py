import datetime as dt
import json


VB_DATES = []


# Create VB Model base class
class VBModel:
    def __init__(self, date, court, time, team):
        self.date = date
        self.court = court
        self.time = time
        self.team = team


# Load vb data
with open("data/volleyball_data_2023.json", "r") as f:
    data = json.load(f)


# Parse saved vb data to vb objects
for item in data:
    line = data[item]
    line_date = [int(value) for value in line["date"]]
    VB_DATES.append(VBModel(dt.date(line_date[0], line_date[1], line_date[2]), line["court"], line["time"], line["team"]))
