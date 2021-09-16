import os
import util

from time import sleep

from selenium import webdriver

from uci.cyclocross.ResultsFrame import ResultsFrame
from uci.cyclocross.Competition import Competition



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
    page.open()
    page.select_racetype("Individual")
    page.select_category("Women Elite")
    page.select_season("2020")

    # only gets results from first page

    page.get_results()

finally:
    sleep(2)
    driver.quit()

