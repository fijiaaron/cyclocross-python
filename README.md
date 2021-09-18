get competitions for season:

		export CYCLOCROSS_SEASON=2022
		python get_competitions_for_season.py

outputs to:
		
		competitions_2022.csv
		competitions_2022.json

get races for competition:
		export CYCLOCROSS_COMPETITION_ID=65009
		python get_races_for_competition.py 

outputs to:
		{competition name} {competition date}.csv
		{competition name} {competition date}.json

download race results:
		
		export CYCLOCROSS_COMPETITION_ID=65009
		export CYCLOCROSS_EVENT_ID=253649
		python download_race_results.py
