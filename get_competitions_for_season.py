import os
import json
import csv

from time import sleep

from selenium import webdriver

from uci.cyclocross.ResultsFrame import ResultsFrame
from uci.cyclocross.Competition import Competition

import util

try:
    log = util.create_logger()

    RUN_HEADLESS = os.getenv("RUN_HEADLESS")
    log.debug("RUN_HEADLESS: {RUN_HEADLESS}")

    options = util.get_chrome_options()
    log.debug(f"chrome options: {options}")
    log.debug(f"headless chrome: {options.headless}")

    driver = webdriver.Chrome(chrome_options = options)
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

    # only gets results from first page (40 rows)
    # this is ok as long as we keep up since it will show newest first
    # in the long run, we might need pagination (tricky)

    # first attempt at pagination (needs tested)

    while page.has_next_page():
        log.debug("getting next page")
        page.go_to_next_page()
        sleep(10)
        more_competitions = page.get_results()
        competitions.extend(more_competitions)
        log.debug(f"# of competitions: {len(competitions)}")

    filename = "competitions_" + season;

    with open(filename + ".json", "w") as jsonfile:
        json.dump(competitions, jsonfile, indent=4)

    with open(filename + ".csv", "w") as csvfile:
        keys = competitions[0].keys()
        csv_writer = csv.DictWriter(csvfile, keys)
        csv_writer.writeheader()
        csv_writer.writerows(competitions)
        
finally:
    sleep(3)
    driver.quit()

