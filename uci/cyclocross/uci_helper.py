from datetime import datetime, timedelta

## Get date info
now = datetime.now()
current_month = now.month
current_year = now.year
current_day_of_year = int(now.strftime("%j"))

def get_season(season) -> str:
    if season == "current":
        #(next year if after July)
        season = current_year
        if current_month > 7: 
            season = current_year + 1
        else:
            season = str(current_year)
    
    return str(season)
