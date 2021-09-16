import logging

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import selenium
expected = selenium.webdriver.support.expected_conditions
present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located
any_visible = expected.visibility_of_any_elements_located



class ResultsFrame:

	url = "https://dataride.uci.org/iframe/results/3"
	timeout = 30

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


	# @staticmethod
	# def visible(self, selector):
	# 	return expected.visibility_of_element_located(selector)


	def __init__(self, driver:WebDriver):
		self.driver = driver
		self.wait = WebDriverWait(self.driver, self.timeout)
		self.setup_logger(__class__.__name__)

	def setup_logger(self, name, level=logging.DEBUG):
		self.log = logging.getLogger(name)
		self.log.addHandler(logging.StreamHandler())
		self.log.addHandler(logging.FileHandler(name + ".log"))



	def open(self):
		self.driver.get(self.url)
		self.wait.until(visible(self.results_heading_selector))



	def choose_element_from_list(elements, matcher):
		return next(filter(lambda element: element.text == matcher, elements))



	def select_racetype(self, racetype="All"):
		racetype_dropdown = self.wait.until(
			expected.element_to_be_clickable(self.racetype_dropdown_selector))
		racetype_dropdown.click()

		racetype_options = self.wait.until(
			expected.visibility_of_all_elements_located(self.racetype_options_selector))

		self.choose_element_from_list(racetype_options, racetype).click()

	def select_category(self, category="All"):
		category_dropdown = wait.until(
			expected.element_to_be_clickable(self.category_dropdown_selector))
		category_dropdown.click()

		category_options = self.wait.until(
			expected.visibility_of_all_elements_located(self.category_options_selector))

		next(filter(lambda option: option.text == category, category_options))


	def select_season(self, season="current"):
		print(f"select season {season}")

		if season == "current":
			print("no action needed for current season")
			return

		print(f"waiting for element to be clickable {self.season_dropdown_arrow_selector}")
		season_dropdown_arrow = wait.until(expected.element_to_be_clickable(self.season_dropdown_arrow_selector))
		print("found season_dropdown_arrow", season_dropdown_arrow)

		print(f"clicking season dropdown {season_dropdown_arrow}")
		season_dropdown_arrow.click()

		print(f"waiting for element to be clickable {self.season_options_selector}")
		season_options = wait.until(
			expected.visibility_of_all_elements_located(self.season_options_selector))
		print(f"found season_options {season_options}")

		print(f"select {season} season option")
		choice = next(filter(lambda option: option.text == season, season_options))
		print(f"filtered option {choice.text}")
		choice.click()
		print(f"clicked option {choice.text} for season")
