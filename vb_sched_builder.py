from datetime import date
import json

dates = []

courts = []

times = []

teams = []


class VBModel:
    def __init__(self, date, court, time, team):
        self.date = date
        self.court = court
        self.time = time
        self.team = team

vb_data = {}

for i, item in enumerate(dates):
    data = {
        "date": dates[i],
        "court": courts[i],
        "time": times[i],
        "team": teams[i]
    }
    vb_data[i] = data

with open("data/volleyball_data.json", "w") as f:
    json.dump(vb_data, f, indent=2)
