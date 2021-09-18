import os
import sys
import argparse
import json
import csv

from time import sleep
from types import SimpleNamespace

from utils import setup

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
expected = expected_conditions
clickable = expected.element_to_be_clickable



# create logger

log = setup.create_logger()


# get environment variables

RUN_HEADLESS = os.getenv("RUN_HEADLESS")
log.debug(f"EVENT_ID: {RUN_HEADLESS}")

EVENT_ID = os.getenv("CYCLOCROSS_EVENT_ID")
log.debug(f"EVENT_ID: {EVENT_ID}")

COMPETITION_ID = os.getenv("CYCLOCROSS_COMPETITION_ID")
log.debug(f"COMPETITION_ID: {COMPETITION_ID}")

DISCIPLINE_ID = "3" # Cyclocross
log.debug(f"DISCIPLINE_ID: {DISCIPLINE_ID}")

if not EVENT_ID:
	print("need to set CYCLOCROSS_EVENT_ID")

if not COMPETITION_ID :
    print("need to set CYCLOCROSS_COMPETITION_ID")
    sys.exit()


# remove old downloads

DOWLOAD_FILE= os.path.expanduser("~/Downloads/Results.xlsx")
log.debug(f"setting download file: {DOWLOAD_FILE}")

if os.path.exists(DOWLOAD_FILE):
	log.debug(f"remove old  file: {DOWLOAD_FILE}" )
	os.remove(DOWLOAD_FILE)


# get race results file from command line arguments
 
my_parser = argparse.ArgumentParser(description="download race results excel file")
my_parser.add_argument('--file',
						help="the competition results json file (csv not supported yet)",
						action='store',
						required=True)

args = my_parser.parse_args()
log.debug(f"file to get race results from: {args.file}")


# load race results from file
races = []
with open(args.file, mode="r") as json_file:
	races = json.load(json_file)

log.debug(f"got {len(races)} races from {json_file.name}")

for race in races:
	race_name = race['race_name']
	race_date = race['date']
	race_category = race['category']
	race_winner = race['winner']
	race_url = race['event_url']

	# race_url = f"https://dataride.uci.org/iframe/EventResults/{EVENT_ID}/{COMPETITION_ID}/{DISCIPLINE_ID}"
	print(f"getting results from url {race_url}")

	export_results_menu_locator = By.CSS_SELECTOR, "#exportMenu"
	export_to_excel_file_locator = By.CSS_SELECTOR, "#exportResultItem"
	competition_link_locator = By.CSS_SELECTOR, "#event-results-view .uci-main-content:first-of-type a"

	# get driver
	chrome_options = setup.get_chrome_options()
	log.debug(f"chrome options: {chrome_options}")
	log.debug(f"headless chrome: {chrome_options.headless}")

	driver = webdriver.Chrome(options = chrome_options)
	log.debug("driver: {driver}")
	log.debug(f"driver capabilities: {driver.capabilities}")

	wait = WebDriverWait(driver, 30)

	# helper function

	def click(locator):
		log.debug(f"click({locator})")
		log.debug(f"wait until clickable {locator}")
		element = wait.until(clickable(locator))
		log.debug("click element: {element}")
		element.click()

	# open race results frame
	driver.get(race_url)

	# get competition info
	competition_link = wait.until(clickable(competition_link_locator))
	competition_name = competition_link.text
	competition_url = competition_link.get_attribute("href")

	log.debug(f"competition: {competition_name}")
	log.debug(f"competition_url: {competition_url}")

	# get additional info
	competition_details = driver.find_element_by_css_selector(".uci-label").text
	log.debug(f"competition details: {competition_details}")

	# download spreadsheet
	wait.until(clickable(export_results_menu_locator)).click()
	wait.until(clickable(export_to_excel_file_locator)).click()

	# close browser
	sleep(15)
	driver.quit()

	# move Results.xml from Downloads to current directory
	competition_filename = race_name + " - " + race_category + " - " + race_date + ".xlsx"
	log.debug(f"moving {DOWLOAD_FILE} to {competition_filename}")
	os.replace(DOWLOAD_FILE, competition_filename)

