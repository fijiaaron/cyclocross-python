import os
from types import SimpleNamespace

from utils import setup
from utils.save_helper import *
from utils.selenium_helper import *
from uci.cyclocross.uci_helper import *
from uci.cyclocross.SeasonResults import SeasonResultsFrame
from uci.cyclocross.CompetitionResults import CompetionsResultsFrame
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

try:
    ## Get Competitions for Season 
    log.debug("get competitions for season")

    racetype = os.getenv("CYCLOCROSS_RACETYPE", default="All")
    category = os.getenv("CYCLOCROSS_CATEGORY", default="All")
    season = os.getenv("CYCLOCROSS_SEASON", default="current")

    season = get_season(season)
    log.debug(f"season: {season}")

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

    log.debug(f"# of competitions: {len(competitions)}")
    
    save_csv(competitions, "xcompetitions", append_date=True)
    save_json(competitions, "xcompetitions", append_date=True)

    ## Cycle through each competition and get results for each category
    for competition in competitions:
        print(competition)
        c = SimpleNamespace(competition)
        print(c)

        competitionResultsFrame = CompetionsResultsFrame(driver, url=c.url)
        competitionResultsFrame


    
except WebDriverException as e:
    print(e)

except Exception as e:
    print(e)

finally:
    driver.quit()


