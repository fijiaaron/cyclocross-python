import setup
from uci.cyclocross.Competition import Competition

from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions

def locator(selector, by = By.CSS_SELECTOR):
	return (by, selector)

def by_css(selector):
	return locator(selector, By.CSS_SELECTOR)

def by_id(id):
	return locator(id, By.ID)

present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located

class CompetitionResultsFrame():

	#url = "https://dataride.uci.org/iframe/CompetitionResults/65045?disciplineId=3"
	timeout = 30

	results_link = By.LINK_TEXT, "Results"
	competition_name = By.CSS_SELECTOR , ".uci-label"
	competition_details = By.CSS_SELECTOR, "ul.uci-detail-list li"
	competition_type = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(1)"
	competition_dates = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(2)"
	competition_category = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(3)"
	competition_city = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(4)"
	competition_country = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(2)"

	def __init__(self, driver:WebDriver, url:str):
		self.log = setup.create_logger(self.__class__.__name__)
		self.driver = driver
		self.wait = WebDriverWait(self.driver, self.timeout)
		self.url = url

	def when_visible(self, locator) -> WebElement:
		self.log.debug(f"when visible {locator}")
		element = self.wait.until(expected.visibility_of_element_located(locator))
		self.log.debug(f"found element {element}")

	def when_all_visible(self, locator) -> List[WebElement]:
		self.log.debug(f"when all visible {locator}")
		elements = self.wait.until(expected.visibility_of_all_elements_located(locator))

	def when_clickable(self, locator) -> WebElement:
		self.log.debug(f"when clickable {locator}")
		return self.wait.until(clickable(locator))


	def open(self):
		self.log.debug(f"open url: {self.url}")
		self.driver.get(self.url)

		competition_name = self.get_competition_name()
		competition_details = self.get_competition_details()

		self.competition = Competition(competition_name, *competition_details)
		self.competition.url = self.url
		self.log.debug(self.competition)

	def get_competition_name(self):
		self.log.debug("get competition name")
		competition_name = self.wait.until(expected.visibility_of_element_located(self.competition_name)).text
		self.log.info(f"competition_name: {competition_name}")
		return competition_name

	def get_competition_details(self):
		self.log.debug("get competition details")
		competition_details = self.wait.until(expected.visibility_of_all_elements_located(self.competition_details))
		competition_type = competition_details[0].text
		competition_dates = competition_details[1].text
		competition_class = competition_details[2].text
		competition_city = competition_details[3].text
		competition_country = competition_details[4].text

		self.log.info(f"competition_type: {competition_type}")
		self.log.info(f"competition_dates: {competition_dates}")
		self.log.info(f"competition_class: {competition_class}")
		self.log.info(f"competition_city: {competition_city}")
		self.log.info(f"competition_country: {competition_country}")

		return (competition_type, competition_dates, competition_class, competition_city, competition_country)

	def get_competition_type(self):
		self.log.info(f"get_competition_type")
		competition_type = self.when_visible(*self.competition_type).text
		self.log.info(f"competition_type: {competition_type}")
		return competition_type

	def get_competition_dates(self):
		self.log.info(f"get_competition_dates")
		competition_dates = self.when_visible(*self.competition_dates).text
		self.log.info(f"competition_dates: {competition_dates}")
		return competition_dates

	def get_competition_class(self):
		self.log.info(f"get_competition_class")
		competition_class = self.when_visible(*self.competition_class).text
		self.log.info(f"competition_class: {competition_class}")
		return competition_class

	def get_competition_city(self):
		self.log.info(f"get_competition_city")
		competition_city = self.when_visible(*self.competition_city).text
		self.log.info(f"competition_city: {competition_city}")
		return competition_city

	def get_competition_country(self):
		self.log.info(f"get_competition_country")
		competition_country = self.when_visible(*self.competition_country).text
		self.log.info(f"competition_country: {competition_country}")
		return competition_country


