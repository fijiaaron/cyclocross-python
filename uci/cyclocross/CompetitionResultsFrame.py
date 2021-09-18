from time import sleep 
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions

from utils import setup
from utils.selenium import *

from uci.cyclocross.Competition import Competition


class CompetitionResultsFrame():

	#url = "https://dataride.uci.org/iframe/CompetitionResults/65045?disciplineId=3"
	timeout = 30

	results_link = By.LINK_TEXT, "Results"
	competition_name = By.CSS_SELECTOR , ".uci-label"
	competition_details = By.CSS_SELECTOR, "ul.uci-detail-list li"
	competition_discipline = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(1)"
	competition_dates = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(2)"
	competition_class = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(3)"
	competition_venue = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(4)"
	competition_country = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(5)"

	results_table_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table"
	table_headers_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > thead [role=columnheader]"
	table_body_locator = locate.by_css(".uci-table-wrapper > table > tbody")
	table_row_locator = locate.by_css(".uci-table-wrapper > table > tbody > tr[role=row]")

	general_classification_link = By.LINK_TEXT, "General Classification"

	main_rows_xpath = By.XPATH, "//table[1]/tbody/tr[contains(@class, 'k-master-row')]"
	detail_rows_xpath = By.XPATH, "//table[1]/tbody/tr[contains(@class, 'k-detail-row')]"

	main_rows_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-master-row"
	detail_rows_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-detail-row"

	collapse_icons_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody [aria-label=Collapse]"
	expand_icons_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody [aria-label=Expand]"

	categories_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-master-row > td:last-of-type"

	def __init__(self, driver:WebDriver, url:str):
		self.log = setup.create_logger(self.__class__.__name__)
		self.driver = driver
		self.wait = WebDriverWait(self.driver, self.timeout)
		self.url = url
	
	def waiter(self, timeout=None) -> WebDriverWait:
		if not timeout:
			return self.wait
		else:
			return WebDriverWait(self.driver, timeout)

	def if_visible(self, locator, timeout=None):
		self.log.debug(f"if_visible({locator}")
		elements = self.when_all_visible(locator, timeout)
		self.log.debug(f"found {len(elements)} element")
		if len(elements) == 1:
			return elements[0]
		return elements

	def when_visible(self, locator, timeout=None) -> WebElement:
		self.log.debug(f"when visible {locator}")
		wait = self.waiter(timeout)
		element = wait.until(visible(locator))
		self.log.debug(f"found element {element}")
		return element


	def when_all_visible(self, locator, timeout=None) -> List[WebElement]:
		self.log.debug(f"when all visible {locator}")
		wait = self.waiter(timeout)
		elements = wait.until(all_visible(locator))
		self.log.debug(f"found {len(elements)} elements")
		return elements


	def when_clickable(self, locator, timeout=None) -> WebElement:
		self.log.debug(f"when clickable {locator}")
		wait = self.waiter(timeout)
		element = wait.until(clickable(locator))
		self.log.debug(f"found element {element}")
		return element

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
		competition_discipline = competition_details[0].text
		competition_dates = competition_details[1].text
		competition_class = competition_details[2].text
		competition_venue = competition_details[3].text
		competition_country = competition_details[4].text

		self.log.info(f"competition_discipline: {competition_discipline}")
		self.log.info(f"competition_dates: {competition_dates}")
		self.log.info(f"competition_class: {competition_class}")
		self.log.info(f"competition_venue: {competition_venue}")
		self.log.info(f"competition_country: {competition_country}")

		return (competition_discipline, competition_dates, competition_class, competition_venue, competition_country)


	def get_competition_discipline(self):
		self.log.info(f"get_competition_discipline")
		competition_discipline = self.when_visible(self.competition_discipline).text
		self.log.info(f"competition_discipline: {competition_discipline}")
		return competition_discipline


	def get_competition_dates(self):
		self.log.info(f"get_competition_dates")
		competition_dates = self.when_visible(self.competition_dates, timeout=10).text
		self.log.info(f"competition_dates: {competition_dates}")
		return competition_dates


	def get_competition_class(self):
		self.log.info(f"get_competition_class")
		competition_class = self.when_visible(self.competition_class, timeout=10).text
		self.log.info(f"competition_class: {competition_class}")
		return competition_class


	def get_competition_venue(self):
		self.log.info(f"get_competition_venue")
		competition_venue = self.when_visible(self.competition_venue, timeout=10).text
		self.log.info(f"competition_venue: {competition_venue}")
		return competition_venue


	def get_competition_country(self):
		self.log.info(f"get_competition_country")
		competition_country = self.when_visible(self.competition_country, timeout=10).text
		self.log.info(f"competition_country: {competition_country}")
		return competition_country


	def get_table_headers(self):
		table_headers = self.when_all_visible(self.table_headers_locator, timeout=10)
		column_names = [header.text for header in table_headers]
		self.log.debug(f"column_names: {column_names}")
		return column_names 


	def get_categories(self):
		category_elements = self.when_all_visible(self.categories_locator, timeout=10)
		self.log.debug(f"# of categories: {len(category_elements)}")
		categories = [category_element.text for category_element in category_elements]
		self.log.debug(f"categories: {categories}") 
		return categories

	def get_race_info(self):
		self.log.debug(f"get_race_info()")
		self.expand_all_rows()

		main_rows = self.when_all_visible(self.main_rows_locator, timeout=1)
		detail_rows = self.when_all_visible(self.detail_rows_locator, timeout=1)

		races = []
		for main_row in main_rows:
			# arrow = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(1) > a")

			# the race name in the table is actually the same as category 
			# race_name = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)").text 

			race_name = self.get_competition_name()
			date = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)").text
			venue = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(4)").text
			category = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(5)").text
			
			self.log.debug(f"race_name: {race_name}, date: {date} venue: {venue}, category: {category}")
			
			
			
			detail_row:WebElement = main_row.find_element(By.XPATH, "./following-sibling::tr[1]")
			self.log.debug("got detail row: " + detail_row.text)
			
			detail_row_wait = WebDriverWait(detail_row, 15)
			race_link = detail_row_wait.until(expected.element_to_be_clickable(self.general_classification_link))
			self.log.debug(f"race_link: {race_link.text} url: {race_link.get_attribute('href')}")

			link:WebElement = detail_row.find_element_by_tag_name("a")
			event_url = link.get_attribute("href")
			self.log.debug(f"event_url: {event_url}")
			
			link_locator = By.XPATH, ".//table/tbody/tr/td[2]"
			winner_locator = By.XPATH, ".//table/tbody/tr/td[2]"

			race_link = detail_row.find_element(*link_locator).get_attribute('href')
			self.log.debug(f"race_link {race_link}")
			winner = detail_row.find_element(*winner_locator).text
			self.log.debug(f"winner {winner}")
			race = {
				'race_name': race_name,
				'date': date,
				'venue': venue,
				'category': category,
				'event_url': event_url,
				'winner': winner
			}
			races.append(race)

		return races

	def expand_all_rows(self):
		self.log.debug(f"expand_all_rows()")
		try:
			expand_links = self.when_all_visible(self.expand_icons_locator, timeout=10)
			self.log.debug(f"expanding {len(expand_links)} rows")
			for link in expand_links:
				link.click()
		except TimeoutException:
			self.log.debug(f"no rows to expand")

		sleep(15)
		links = self.wait.until(all_visible(self.general_classification_link))
		self.log.debug(f"race links {len(links)}")

	def collapse_all_rows(self):
		self.log.debug(f"collapse_all_rows")
		
		try:
			collapse_links = self.when_all_visible(self.collapse_icons_locator, timeout=10)
			self.log.debug(f"collapsing {len(collapse_links)} rows")
			for link in collapse_links:
				link.click()
		except:
			self.log.debug(f"no rows to collapse")
