import logging
import json
import re

from typing import List, Tuple, Dict, Set, Optional

from types import SimpleNamespace

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions
present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located
any_visible = expected.visibility_of_any_elements_located

import util

class ResultsFrame:

	url = "https://dataride.uci.org/iframe/results/3"
	timeout = 20

	results_heading_selector = (By.CSS_SELECTOR, ".uci-label")

	racetype_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=raceTypes_listbox] [class*=arrow]")
	racetype_dropdown_selector = (By.CSS_SELECTOR, "#raceTypes")
	racetype_options_selector = (By.CSS_SELECTOR, "#raceTypes_listbox li")
	racetype_option_selected = (By.CSS_SELECTOR, "#raceTypes_listbox li[aria-selected=true]")

	category_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=categories_listbox] [class*=arrow]")
	category_dropdown_selector = (By.CSS_SELECTOR, "#categories")
	category_options_selector = (By.CSS_SELECTOR, "#categories_listbox li")
	category_option_selected = (By.CSS_SELECTOR, "#categories_listbox li[aria-selected=true]")

	season_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=seasons_listbox] [class*=arrow]")
	season_dropdown_selector = (By.CSS_SELECTOR, "#seasons")
	season_options_selector = (By.CSS_SELECTOR, "#seasons_listbox li")
	season_option_selected = (By.CSS_SELECTOR, "#seasons_listbox li[aria-selected=true]")

	date_table_header_selector = (By.CSS_SELECTOR, "[data-title=Date]")
	competition_table_header_selector = (By.CSS_SELECTOR, "[data-title=Competition]")
	country_table_header_selector = (By.CSS_SELECTOR, "[data-title=Country]")
	class_table_header_selector = (By.CSS_SELECTOR, "[data-title=Class]")

	loading_selector = (By.CSS_SELECTOR, ".k-loading-mask")
	competition_table_row_selector = (By.CSS_SELECTOR, "#competitions table tbody tr")
	

	def __init__(self, driver:WebDriver):
		self.driver = driver
		self.wait = WebDriverWait(self.driver, self.timeout)
		self.log = util.create_logger(__class__.__name__)
		self.log.debug(f"initialized")


	def open(self) -> ResultsFrame:
		self.log.debug(f"open {__class__.__name__}")
		self.driver.get(ResultsFrame.url)
		self.wait.until(visible(self.results_heading_selector))
		self.log.debug(f"got title: {self.driver.title}")

		return self


	def when_visible(self, locator) -> WebElement:
		self.log.debug(f"when_visible({locator})")
		
		if isinstance(locator, WebElement):
			element = locator
			return self.wait.until(expected.visibility_of(element))
			
		self.log.debug(f"locating {locator}")
		return self.wait.until(expected.visibility_of_element_located(locator))
				

	def when_all_visible(self, locator) -> List[WebElement]:
		self.log.debug(f"when_all_visible({locator})")
		
		self.log.debug(f"locating {locator}")
		return self.wait.until(expected.visibility_of_all_elements_located(locator))
		

	def when_clickable(self, locator) -> WebElement:
		self.log.debug(f"when_clickable({locator})")
		
		if isinstance(locator, WebElement):
			element = locator
			self.wait.until(expected.element_to_be_clickable(element))

		self.log.debug(f"locating {locator}")
		return self.wait.until(expected.element_to_be_clickable(locator))


	def choose_element_from_list(self, elements, matcher) -> WebElement:
		return next(filter(lambda element: element.text == matcher, elements))


	def select_racetype(self, racetype="All", forceSelection=False):
		self.log.debug(f"select racetype: {racetype}")
		self.racetype = racetype
	
		if racetype == "All" and not forceSelection:
			self.log.debug("doing nothing - default racetype should be selected")

		racetype_dropdown = self.when_clickable(self.racetype_dropdown_arrow_selector)

		self.log.debug(f"click racetype_dropdown: {racetype_dropdown}")
		racetype_dropdown.click()

		racetype_options = self.when_all_visible(self.racetype_options_selector)
		
		self.log.debug(f"choose racetype from racetype_options: {racetype_options}")
		self.choose_element_from_list(racetype_options, racetype).click()

		self.log.debug(f"wait loading mask indicate refreshed data")
		self.wait.until(expected.visibility_of_element_located(self.loading_selector))
		self.wait.until_not(expected.presence_of_element_located(self.loading_selector))

	def select_category(self, category="All", forceSelection=False):
		self.log.debug(f"select_category({category}")
		self.category = category

		if category == "All" and not forceSelection:
			self.log.debug("doing nothing - default category should be selected")
			return 

		category_dropdown = self.when_clickable(self.category_dropdown_arrow_selector)

		self.log.debug(f"click category dropdown: {category_dropdown}")
		category_dropdown.click()

		category_options = self.when_all_visible(self.category_options_selector)

		self.log.debug(f"choose category from category_options: {category_options}")
		self.choose_element_from_list(category_options, category).click()

		self.log.debug(f"wait loading mask indicate refreshed data")
		self.wait.until(expected.visibility_of_element_located(self.loading_selector))
		self.wait.until_not(expected.presence_of_element_located(self.loading_selector))


	def select_season(self, season="current", forceSelection=False):
		self.log.debug(f"select_season({season})")
		self.season = season

		if season == "current" and not forceSelection:
			self.log.debug("doing nothing - default season should be selected")
			return

		self.log.debug(f"waiting for element to be clickable {self.season_dropdown_arrow_selector}")
		season_dropdown = self.when_clickable(self.season_dropdown_arrow_selector)

		self.log.debug(f"click season dropdown {season_dropdown}")
		season_dropdown.click()

		season_options = self.when_all_visible(self.season_options_selector)

		self.log.debug(f"choose season from season_options: {season_options}")
		self.choose_element_from_list(season_options, season).click()

		self.log.debug(f"wait loading mask indicate refreshed data")
		self.wait.until(expected.visibility_of_element_located(self.loading_selector))
		self.wait.until_not(expected.presence_of_element_located(self.loading_selector))


	def get_results(self):
		rows = self.when_all_visible(self.competition_table_row_selector)
		self.log.debug("rows: {len(rows)")
		for row in rows:
			self.log.debug(f"row: {row.text}")

			cells:List[WebElement] = row.find_elements(By.TAG_NAME, "td")
			
			competition = {
				"date" : cells[0].text,
				"competition" : cells[1].text,
				"url" : cells[1].get_attribute("href"),
				"country" : cells[2].text,
				"competition_class" : cells[3].text,
				"season" : self.season 
			}

			self.log.debug()

	@staticmethod
	def id_from_url(url):
		match = re.search("^http.*/CompetitionResults/(\d+)/.*$", url)

		if match and match.groups() and len(match.groups()) == 1:
			return match.groups()[0]
		else:
			raise Exception("URL does not look like CompetitionResults")
