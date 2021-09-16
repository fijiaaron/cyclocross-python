# get_competitions_results.py

import sys
import logging
from types import FunctionType

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected

### create logger
def create_logger(name=__name__):
	log = logging.getLogger(name)
	log.setLevel(logging.DEBUG)

	datetimeFormat = "%Y%m%d.%H%M%S"
	logFormat = " %(asctime)s.%(msecs)03d | %(filename)s:%(lineno)d | %(name)s | %(levelname)-8.8s | %(message)s"
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	console_log = True
	if console_log:
		console_log_handler = logging.StreamHandler(sys.stdout)
		console_log_handler.setFormatter(logFormatter)
		log.addHandler(console_log_handler)
		log.debug(f"console log added")

	log_file = __name__ + ".log"
	if log_file:
		file_log_handler = logging.FileHandler(log_file)
		file_log_handler.setFormatter(logFormatter)
		log.addHandler(file_log_handler)
		log.debug(f"file log added: {log_file}")

	log.debug(f"created logger: {log}")
	return log



log = create_logger()



### create webdriver instance
def create_webdriver():
	log.debug(f"creating WebDriver instance")
	driver = webdriver.Chrome()
	log.debug(f"driver {driver}")

### create webdriverwait instance
def create_webdriverwait(driver, timeout=30):
	log.debug(f"creating WebDriverWait instance")
	log.debug(f"timeout", timeout)
	wait = WebDriverWait(driver, timeout)
	log.debug(f"wait", wait)
	return wait



driver = create_webdriver()
wait = create_webdriverwait(driver)


def present(locator, by=By.CSS_SELECTOR):
	log.debug(f"expected presence of element located {by} {locator}")
	return expected.presence_of_element_located(by, locator)

def visible(locator, by=By.CSS_SELECTOR):
	log.debug(f"expected visibility of element located {by} {locator}")
	return expected.visibility_of_element_located(by, locator)

def clickable(locator, by=By.CSS_SELECTOR):
	log.debug(f"expected element to be clickable located {by} {locator}")
	return expected.element_to_be_clickable(by, locator)

def all_present(locator, by=By.CSS_SELECTOR):
	log.debug(f"expected presence of all elements located {by} {locator}")
	return expected.presence_of_all_elements_located(by, locator)

def all_visible(locator, by=By.CSS_SELECTOR):
	log.debug(f"expected visibility of all elements located {by} {locator}")
	return expected.visibility_of_all_elements_located(by, locator)



def when_present(locator, by=By.CSS_SELECTOR) -> WebElement:
	log.debug(f"wait until ...")
	return wait.until(present(locator, by))

def when_visible(locator, by=By.CSS_SELECTOR) -> WebElement:
	log.debug(f"wait until ...")
	return wait.until(present(locator, by))

def when_clickable(locator, by=By.CSS_SELECTOR) -> WebElement:
	log.debug(f"wait until ...")
	return wait.until(present(locator, by))

def when_all_present(locator, by=By.CSS_SELECTOR) -> WebElement:
	log.debug(f"wait until ...")
	return wait.until(all_present(locator, by))

def when_all_visible(locator, by=By.CSS_SELECTOR) -> WebElement:
	log.debug(f"wait until ...")
	return wait.until(all_present(locator, by))



def when(locator, condition:FunctionType=visible, by=By.CSS_SELECTOR):
	log.debug(f"wait until {condition.__name__}, {locator}")
	return wait.until(condition(by, locator))

def open_page(driver, url):
	log.debug(f"opening uci cyclocross results page")
	uci_cyclocross_results_url = "https://dataride.uci.org/iframe/results/3"
	log.debug(f"uci_cyclocross_results_url {uci_cyclocross_results_url}")
	driver.get(uci_cyclocross_results_url)

	log.debug(f"current_url {driver.current_url}")
	log.debug(f"title {driver.title}")

	heading = wait.until(expected.presence_of_element_located(By.CSS_SELECTOR, ".uci-label"))
	log.debug("")

def get_competitions_for_season(driver):
	wait.until(expected.pre)

try:
	driver = create_webdriver()
	wait = create_webdriverwait(driver)
	page = open_page()


except:
	log.warn("something went wrong")

finally:
	driver.quit()


