import os
import sys
import json
import csv

from types import SimpleNamespace 


from utils import setup
from uci.cyclocross.CompetitionResultsFrame import CompetitionResultsFrame

from selenium import webdriver

# create logger
log = setup.create_logger()

# get driver
chrome_options = setup.get_chrome_options()
log.debug(f"chrome options: {chrome_options}")
log.debug(f"headless chrome: {chrome_options.headless}")

driver = webdriver.Chrome(options = chrome_options)
log.debug("driver: {driver}")
log.debug(f"driver capabilities: {driver.capabilities}")

# get competition

## need to data drive
## for competition in competitions:
COMPETITION_ID= os.getenv("CYCLOCROSS_COMPETITION_ID")
DISCIPLINE_ID = "3" # Cyclocross

if not COMPETITION_ID:
    print("need to set CYCLOCROSS_COMPETITION_ID")
    sys.exit()


competition_results_url = f"https://dataride.uci.org/iframe/CompetitionResults/{COMPETITION_ID}?disciplineId={DISCIPLINE_ID}"
print(f"getting results from  url {competition_results_url}")

# get results
page = CompetitionResultsFrame(driver, competition_results_url)
page.open()

competition_name = page.get_competition_name()
competition_discipline = page.get_competition_discipline()
competition_dates = page.get_competition_dates()
competition_class = page.get_competition_class()
venue = page.get_competition_venue()
country = page.get_competition_country()

headers = page.get_table_headers()
categories = page.get_categories()
# page.expand_all_rows()

races = page.get_race_info()

# close driver
driver.quit()

# print results
print(races)
# event_results = [SimpleNamespace(**race) for race in races]
# print(event_results)

# save results 
date = str(competition_dates).split("-")[1].strip()
filename = competition_name + " " + date

# export to JSONs
with open(filename + ".json", mode="w", encoding="utf8") as jsonfile:
    json.dump(races, jsonfile, indent=4, ensure_ascii=False)
    print(jsonfile.name)

# export to CSV    
with open(filename + ".csv", mode="w") as csvfile:
    keys = races[0].keys()
    csv_writer = csv.DictWriter(csvfile, keys)
    csv_writer.writeheader()
    csv_writer.writerows(races)
    print(csvfile.name)