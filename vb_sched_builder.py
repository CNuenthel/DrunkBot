from datetime import date
import json

dates = [
    ["2023", "05", "17"],
    ["2023", "05", "24"],
    ["2023", "05", "31"],
    ["2023", "06", "07"],
    ["2023", "06", "14"],
    ["2023", "06", "21"],
    ["2023", "06", "28"]]

courts = [
    5, 6, 5, 5, 5, 6, 5
]

times = [
    "7:15",
    "6:10",
    "8:20",
    "6:10",
    "7:15",
    "7:15",
    "7:15"
]

teams = [
    "Digging Doves",
    "Frank Lloyd Spike",
    "Sets With The Lights On",
    "The Bobby Pins",
    "One Hit Wonder",
    "UNDeniable",
    "Yung Professionals"
]


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

with open("volleyball_data_2023.json", "w") as f:
    json.dump(vb_data, f, indent=2)
