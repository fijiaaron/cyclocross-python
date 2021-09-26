# utils/setup.py

import os
import sys
import logging

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	'''
		Create logging instance
		Sets log format and date format

		Arguments:
			name:str default="LOG"
			file:str default=None log to file if filename is included
			console:bool default=True log to console if true
			leve:str default="DEBUG" logging level
		Returns:
			logging 
	'''

	# create logger
	logger = logging.getLogger(name)
	logger.setLevel(level)

	# set log and date format
	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(levelname)-8.8s | %(name)s#%(funcName)s| %(filename)s:%(lineno)d | %(message)s'
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	# add logging handlers -- make sure to avoid duplicates
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


# Create instance of logger
log = create_logger(__name__)

# setup date info
now = datetime.now()
today = now.date()
current_month = now.month
current_year = now.year
current_day_of_year = int(now.strftime("%j"))

def datestamp(dt=None, format="%Y-%m-%d") -> str:
	'''
	get date in format "2021-01-31"
	
	Arguments:
		dt - the datetime -- defaults to now
		format - the datetime format -- defaults to "%Y-%m-%d"
	'''
	if not dt:
		dt = datetime.now()
	return dt.strftime(format)

def dateformat(dt=None, format="%d %b %Y") -> str:
	'''
	get date in format "01 Jan 2021" 
	Arguments:
		dt - the datetime -- defaults to now
		format - the datetime format -- defaults to "%d %b %Y"
	'''
	if not dt:
		dt = datetime.now()
	return dt.strftime(format)


def get_chrome_options(headless:bool=False, downloads:str="/tmp") -> Options:
	'''
	Get Chrome Options
	optionally run headless
	set downloads directory
	
	Args:
		headless (bool) False - Run chrome headless
		downloads (str) /tmp - Chrome downloads directory
		
	Returns:
		Options - chrome options
	'''
	
	# create chrome options
	chrome_options = Options()

	# set download directory to /tmp
	chrome_prefs = {
		"download.default_directory": downloads,
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing.enabled": True
	}

	# define headless options    
	if headless:
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--disable-gpu")

		# disable images
		chrome_prefs["profile.default_content_settings"] = {"images": 2}
		chrome_prefs["download.default_directory"] = "/tmp"

	chrome_options.experimental_options["prefs"] = chrome_prefs

	return chrome_options


def get_chromedriver(chrome_options:Options=None) -> WebDriver:
	'''
		get chromedriver instance
		add chrome options 
		or fetch from get_chrome_options()
	'''

	# set chrome options
	if chrome_options == None:
		chrome_options = get_chrome_options()
	log.debug(f"chrome_options: {chrome_options}")

	# create driver instance
	driver = webdriver.Chrome(chrome_options=chrome_options)
	log.debug(f"driver: {driver}")

	return driver
	