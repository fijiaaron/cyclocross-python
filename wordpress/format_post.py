import os
import glob
import json
from types import SimpleNamespace

files =  glob.glob('results/*.json')

for file in files:
    if "competition" not in file:
        print(file)
        
        with open(file) as races_json_file:
            races = json.load(races_json_file)
            for race_dict in races:
                race = SimpleNamespace(**race_dict)
                print(f"2021 {race.race_name} in {race.venue} cyclocross results: {race.category}")
                print()
                print(f"On {race.date}, {race.race_name} was hosted in {race.venue}. Here are the results for {race.category}.")
                print("\n\n")