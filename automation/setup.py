import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

RUN_HEADLESS = os.getenv('RUN_HEADLESS') in ("TRUE", "True", "true", "YES", "Yes", "yes", "1", 1, True)

def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(filename)s:%(lineno)d | %(module)s.%(name)s.%(funcName)s | %(levelname)-8.8s | %(message)s'
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	if console:
		console_log_handler = logging.StreamHandler()
		console_log_handler.setFormatter(logFormatter)
		logger.addHandler(console_log_handler)

	if file:
		logFile = "logtest.py.log"
		file_log_handler = logging.FileHandler(logFile)
		file_log_handler.setFormatter(logFormatter)
		logger.addHandler(file_log_handler)

	return logger


log = create_logger(__file__)

def get_chrome_options(headless:bool=None) -> Options:
	log.debug(f"get_chrome_options...")


	if RUN_HEADLESS and headless == None:
		headless = RUN_HEADLESS
		log.debug(f"headless: {RUN_HEADLESS}")

	headless_chrome_options = Options()
	headless_chrome_options.add_argument("--headless")
	headless_chrome_options.add_argument("--no-sandbox")
	headless_chrome_options.add_argument("--disable-dev-shm-usage")

	# disable images
	headless_chrome_prefs = {}
	headless_chrome_prefs["profile.default_content_settings"] = {"images": 2}
	headless_chrome_options.experimental_options["prefs"] = headless_chrome_prefs

	if headless:
		log.debug(f"headless: {headless}")
		return headless_chrome_options
	else:
		return Options()

def get_chromedriver(chrome_options=None) -> WebDriver:
	log.debug("get_chromedriver...")

	if chrome_options == None:
		chrome_options = get_chrome_options()

	log.debug("chrome_options: ", chrome_options)

	driver = webdriver.Chrome(chrome_options)
	log.debug("driver: ", driver)
