# util.py

import os
import sys
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver





def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(name)s | %(filename)s:%(lineno)d | %(levelname)-8.8s | %(message)s'
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	if not logger.handlers:
		if console:
			console_log_handler = logging.StreamHandler(sys.stdout)
			console_log_handler.setFormatter(logFormatter)
			logger.addHandler(console_log_handler)
		if file:
			logFile = "logtest.py.log"
			file_log_handler = logging.FileHandler(logFile)
			file_log_handler.setFormatter(logFormatter)
			logger.addHandler(file_log_handler)

	return logger


log = create_logger(__name__)

def get_chrome_options(headless:bool=None) -> Options:
	log.debug("get_chrome_options...")

	RUN_HEADLESS = os.getenv('RUN_HEADLESS', False) in ("TRUE", "True", "true", "YES", "Yes", "yes", "1", 1, True)
	log.debug(f"RUN_HEADLESS {RUN_HEADLESS}")

	if RUN_HEADLESS and not headless:
		log.debug(f"RUN_HEADLESS: {RUN_HEADLESS}")
		headless = RUN_HEADLESS
		log.debug(f"headless: {str(headless)}")
	else:
		log.debug(f"headless is not set")


	headless_chrome_options = Options()
	headless_chrome_options.add_argument("--headless")
	headless_chrome_options.add_argument("--no-sandbox")
	headless_chrome_options.add_argument("--disable-dev-shm-usage")

	# disable images
	headless_chrome_prefs = {}
	headless_chrome_prefs["profile.default_content_settings"] = {"images": 2}
	headless_chrome_options.experimental_options["prefs"] = headless_chrome_prefs

	if headless:
		return headless_chrome_options
	else:
		return Options()

def get_chromedriver(chrome_options:Options=None) -> WebDriver:
	log.debug(f"get_chromedriver...")

	if chrome_options == None:
		chrome_options = get_chrome_options()

	log.debug(f"chrome_options: {chrome_options}")

	driver = webdriver.Chrome(chrome_options=chrome_options)
	log.debug(f"driver: {driver}")
