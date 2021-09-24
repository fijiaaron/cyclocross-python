# setup.py

import os
import sys
import logging

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

expected = expected_conditions
present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located


def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(name)s#%(funcName)s| %(filename)s:%(lineno)d | %(levelname)-8.8s | %(message)s'
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


def get_chrome_options(headless:bool=False, downloads:str="/tmp"):
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



def get_chromedriver(chrome_options:Options=None) -> WebDriver:
	log.debug(f"get_chromedriver...")

	if chrome_options == None:
		chrome_options = get_chrome_options()


	log.debug(f"chrome_options: {chrome_options}")

	driver = webdriver.Chrome(chrome_options=chrome_options)
	
	log.debug(f"driver: {driver}")
	return driver
	