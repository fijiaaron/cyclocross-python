import logging
import json
import re
from sys import stdout
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions
clickable = expected.element_to_be_clickable
visible = expected.visibility_of_element_located
all_visible = expected.visibility_of_all_elements_located


def create_logger(name:str="LOG", file:str=None, console:bool=True, level:str="DEBUG"):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	datetimeFormat = '%Y%m%d.%H%M%S'
	logFormat = ' %(asctime)s.%(msecs)03d | %(name)s | %(filename)s:%(lineno)d | %(module)s.%(funcName)s | %(levelname)-8.8s | %(message)s'
	logFormatter = logging.Formatter(logFormat, datefmt=datetimeFormat)

	if console:
		console_log_handler = logging.StreamHandler(stdout)
		console_log_handler.setFormatter(logFormatter)
		logger.addHandler(console_log_handler)

	if file:
		logFile = "logtest.py.log"
		file_log_handler = logging.FileHandler(logFile)
		file_log_handler.setFormatter(logFormatter)
		logger.addHandler(file_log_handler)

	return logger


	competition_url = "https://dataride.uci.org/iframe/CompetitionResults/65009/3/"

class Competition:
	def __init__(self, name=None, type=None, dates=None, _class=None, venue=None, country=None, url=None, id=None, season=None):
		self.competition_name = name
		self.competition_type = type
		self.competition_dates = dates
		self.competition_class = _class
		self.competition_venue = venue
		self.competition_country = country
		self.competition_url =  url
		self.competition_id = id
		self.competition_season = season

	@staticmethod
	def url_from_id(id):
		return f"https://dataride.uci.org/iframe/CompetitionResults/{id}/3/"

	@staticmethod
	def id_from_url(url):
		match = re.search("^http.*/CompetitionResults/(\d+)/.*$", url)

		if match and match.groups() and len(match.groups()) == 1:
			return match.groups()[0]
		else:
			raise Exception("URL does not look like CompetitionResults")

class CompetitionResults:

	results_link_locator = By.LINK_TEXT, "Results"
	competition_heading_locator = By.CSS_SELECTOR, ".uci-label"
	competition_details_locator = By.CSS_SELECTOR, ".uci-detail-list li"
	competition_type_locator = By.CSS_SELECTOR, ".uci-detail-list li:nth-of-type(1)"
	competition_dates_locator = By.CSS_SELECTOR, ".uci-detail-list li:nth-of-type(2)"
	competition_class_locator = By.CSS_SELECTOR, ".uci-detail-list li:nth-of-type(3)"
	competition_venue_locator = By.CSS_SELECTOR, ".uci-detail-list li:nth-of-type(4)"
	competition_country_locator = By.CSS_SELECTOR, ".uci-detail-list li:nth-of-type(5)"

	competition_results_table_locator = By.CSS_SELECTOR, ".uci-table-wrapper table"

	def __init__(self, driver, competition_url, timeout=30):
		self.driver = driver
		self.wait = WebDriverWait(driver, timeout)
		self.url = competition_url
		self.log = create_logger(self.__class__.__name__)
		self.log.debug(f"initializing...")

	def create_log(self):
		log = logging.getLogger(__class__.__name__)

	def open(self):
		self.log.debug(f"opening {self.url}")
		self.driver.get(self.url)
		self.log.debug(f"current url: {driver.current_url}")

		self.wait.until(visible(self.competition_results_table_locator))

		self.results_link = self.get_results_link()

		self.competition_heading = self.get_competition_heading()
		self.log.debug(f"competition: {self.competition_heading.text}")

		self.competition_details = self.get_competition_details()
		self.log.debug(f"competition details: {self.competition_details}" )
		details = [element.text for element in self.competition_details]
		self.log.debug(f"{details}")

		self.competition_name = self.get_competition_name()
		self.competition_type = self.get_competition_type()
		self.competition_dates = self.get_competition_dates()
		self.competition_class = self.get_competition_class()
		self.competition_venue = self.get_competition_venue()
		self.competition_country = self.get_competition_country()

		self.competition = Competition(
			url = self.url,
			name = self.competition_name,
			type = self.competition_type,
			dates = self.competition_dates,
			_class = self.competition_class,
			)

		return self

	def get_results_link(self) -> WebElement:
		self.log.debug(f"get_results_link()...")
		return self.wait.until(clickable(self.results_link_locator))

	def get_competition_heading(self) -> WebElement :
		self.log.debug(f"get_competition_heading()...")
		return self.wait.until(visible(self.competition_heading_locator))

	def get_competition_details(self) -> List[WebElement]:
		self.log.debug(f"get_competition_details()...")
		return self.wait.until(all_visible(self.competition_details_locator))

	def get_element_text(self, locator) -> str:
		element:WebElement = self.wait.until(visible(locator))
		self.log.debug(f"element: {element}")
		self.log.debug(f"text: {element.text}")
		return element.text

	def get_competition_name(self) -> str:
		return self.get_element_text(self.get_competition_heading())

	def get_competition_type(self) -> str:
		self.log.debug(f"get_competition_type()...")
		return self.get_element_text(self.competition_type_locator)

	def get_competition_dates(self) -> str:
		self.log.debug(f"get_competition_dates()...")
		return self.get_element_text(self.competition_dates_locator)

	def get_competition_class(self) -> str:
		self.log.debug(f"get_competition_class())...")
		return self.get_element_text(self.competition_class_locator)

	def get_competition_venue(self) -> str:
		self.log.debug(f"get_competition_venue()...")
		return self.get_element_text(self.competition_venue_locator)

	def get_competition_country(self) -> str:
		self.log.debug(f"get_competition_country()...")
		return self.get_element_text(self.competition_country_locator)


# launch webdriver

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

# open competition url
competition_page = CompetitionResults(driver, competition_url=competition_url)
competition_page.open()

# get link back to results
results_link =  wait.until(clickable(CompetitionResults.results_link_locator))
results_link_text = results_link.text
results_link_url = results_link.get_attribute("href")
print(f"Results link: {results_link_text} {results_link_url}")

print(json.dumps(competition_page.__dict__))
