import os
from time import sleep
from types import SimpleNamespace

from utils import setup
from utils.file_helper import *
from utils.selenium_helper import *
from uci.cyclocross.uci_helper import *
from uci.cyclocross.SeasonResults import SeasonResultsFrame
from uci.cyclocross.CompetitionResults import CompetitionResultsFrame
from uci.cyclocross.EventResults import EventResultsFrame

## Start logger
log = setup.create_logger(__name__)
log.info("starting")

## Get Chrome driver instance
RUN_HEADLESS = os.getenv("RUN_HEADLESS")
log.debug(f"RUN_HEADLESS: {RUN_HEADLESS}")

chrome_options = setup.get_chrome_options()
log.debug(f"chrome options: {chrome_options}")
log.debug(f"headless chrome: {chrome_options.headless}")

driver = setup.get_chromedriver(chrome_options = chrome_options)
log.debug("driver: {driver}")
log.debug(f"driver capabilities: {driver.capabilities}")


racetype = os.getenv("CYCLOCROSS_RACETYPE", default="All")
category = os.getenv("CYCLOCROSS_CATEGORY", default="All")
season = os.getenv("CYCLOCROSS_SEASON", default="current")

season = get_season(season)
log.debug(f"season: {season}")


try:
	## Get Competitions for Season 
	log.debug(f"get competitions for season {season}")

	seasonResultsFrame = SeasonResultsFrame(driver)
	seasonResultsFrame.open()

	seasonResultsFrame.select_racetype(racetype)
	seasonResultsFrame.select_category(category)
	seasonResultsFrame.select_season(season)
	
	### Gets competitions
	competitions = seasonResultsFrame.get_results()

	### Cycle through paginated results
	max_pages = 3
	current_page = seasonResultsFrame.get_current_page_number()

	if seasonResultsFrame.has_next_page() and current_page <= max_pages:
		seasonResultsFrame.go_to_next_page()
		more_competitions = seasonResultsFrame.get_results()
		competitions.extend(competitions)

	log.debug(f"got {len(competitions)} competitions")
	
	filename = "competitions_" + season + "_season_"
	save_csv(competitions, filename, filepath="xresults", append_date=True)
	save_json(competitions,filename, filepath="xresults", append_date=True)
	log.debug("finished_save_json)")
	
	log.debug("cycling through competitions")
	
	## Cycle through each competition and get results for each category of event ('e.g. Men Elite, etc)
	for competition in competitions:
		log.debug(f"competition {competition}")

		c = SimpleNamespace(**competition)
		log.debug(f"get event results for competition at url {c.url}")
		
		competitionResultsFrame = CompetitionResultsFrame(driver, url=c.url)
		log.debug("competitionResultsFrame Created")

		competitionResultsFrame.open()

		competition_name = competitionResultsFrame.get_competition_name()
		competition_discipline = competitionResultsFrame.get_competition_discipline()
		competition_dates = competitionResultsFrame.get_competition_dates()
		competition_class = competitionResultsFrame.get_competition_class()
		competition_venue = competitionResultsFrame.get_competition_venue()
		competition_country = competitionResultsFrame.get_competition_country()

		headers = competitionResultsFrame.get_table_headers()
		categories = competitionResultsFrame.get_categories()

		events = competitionResultsFrame.get_event_results()
		log.debug(f"got {len(events)} of events")

		filename = "events_" + competition_name
		save_csv(events, filename, filepath="xresults", append_date=True)
		save_json(events, filename, filepath="xresults", append_date=True)

		# cycle through events for a competition and download the results XLSX file
		for event in events:
			e = SimpleNamespace(**event)
			print(f"event: {e}")

			log.debug(f"downloading event Results.xlsx for event {e} at url: {e.url}")

			# remove old downloads
			DOWLOAD_FILE= os.path.expanduser("/tmp/Results.xlsx")
			log.debug(f"setting download file: {DOWLOAD_FILE}")

			if os.path.exists(DOWLOAD_FILE):
				log.debug(f"remove old file: {DOWLOAD_FILE}" )
				os.remove(DOWLOAD_FILE)

			# open EventResultsFrame
			eventResultsFrame = EventResultsFrame(driver, e.url)
			eventResultsFrame.open()
			
			# download file
			eventResultsFrame.download_results_excel()
			sleep(10)
			
			log.debug(f"e.competition_name: {e.competition_name}")
			log.debug(f"e.category: {e.category}")
			log.debug(f"e.date: {e.date}")
			
			results_filename = "xresults/results_" \
						+ e.competition_name + "_" \
						+ e.category + "_" \
						+ e.date \
						+ ".xlsx"

			# move Results.xml from Downloads to currecompetition_class_locatoresults_excel_filename = competition_name + " - " +  + " - " + race_date + ".xlsx"
			log.debug(f"moving {DOWLOAD_FILE} to {results_filename}")
			os.replace(DOWLOAD_FILE, results_filename)

			sleep(10)
			
					
except WebDriverException as e:
	print(e)

except Exception as e:
	print(e)

finally:
	driver.quit()