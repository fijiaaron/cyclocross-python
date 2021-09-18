import os
import json
import csv

from time import sleep

from selenium import webdriver

from uci.cyclocross.ResultsFrame import ResultsFrame

from utils import setup

try:
    log = setup.create_logger()

    RUN_HEADLESS = os.getenv("RUN_HEADLESS")
    log.debug(f"RUN_HEADLESS: {RUN_HEADLESS}")

    chrome_options = setup.get_chrome_options()
    log.debug(f"chrome options: {chrome_options}")
    log.debug(f"headless chrome: {chrome_options.headless}")

    driver = webdriver.Chrome(options = chrome_options)
    log.debug("driver: {driver}")
    log.debug(f"driver capabilities: {driver.capabilities}")

    page = ResultsFrame(driver)

    racetype = os.getenv("CYCLOCROSS_RACETYPE", default="All")
    category = os.getenv("CYCLOCROSS_CATEGORY", default="All")
    season = os.getenv("CYCLOCROSS_SEASON", default="current")

    page.open()
    #sleep(30)
    page.select_racetype(racetype)
    # sleep(10)
    page.select_category(category)
    # sleep(10)
    page.select_season(season)
    # sleep(30)


    competitions = page.get_results()
    log.debug(f"# of competitions: {len(competitions)}")

    # cycle through pagination 

    while page.has_next_page():
        log.debug("getting next page")
        page.go_to_next_page()
        sleep(10)
        more_competitions = page.get_results()
        competitions.extend(more_competitions)
        log.debug(f"# of competitions: {len(competitions)}")

    filename = "competitions_" + season;

    with open(filename + ".json", mode="w", encoding="utf8") as jsonfile:
        json.dump(competitions, jsonfile, indent=4, ensure_ascii=False)

    with open(filename + ".csv", mode="w") as csvfile:
        keys = competitions[0].keys()
        csv_writer = csv.DictWriter(csvfile, keys)
        csv_writer.writeheader()
        csv_writer.writerows(competitions)
        
finally:
    sleep(3)
    driver.quit()

