# basic.py

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected



## Open Cyclcross Results Frame

driver = webdriver.Chrome()
timeout = 15
wait = WebDriverWait(driver, timeout)

results_url = "https://dataride.uci.org/iframe/results/3"
driver.get(results_url)

results_heading_locator = By.CSS_SELECTOR, ".uci-label"
heading = wait.until(expected.visibility_of(results_heading_locator))


## Select Paramters

def choose_element_from_list(elements, matcher):
	return next(filter(lambda element: element.text == matcher, elements))

## Select RaceType

def select_racetype(driver, raceType):
	racetype_dropdown = wait.until(expected.element_to_be_clickable((By.CSS_SELECTOR, "[aria-owns=raceTypes_listbox]")))
	expanded = racetype_dropdown.get_attribute("aria-expanded") == "true"
	if not expanded:
		racetype_dropdown.click()

	racetype_options = wait.until(expected.visibility_of_all_elements_located((By.CSS_SELECTOR, "#raceTypes_listbox li")))
	choose_element_from_list(racetype_options, raceType).click()

	racetype_option_selected_locator = (By.CSS_SELECTOR, "#raceTypes_listbox li[aria-selected=true]")
	racetype_option_selected = driver.find_element(*racetype_option_selected_locator)
	print(f"racetype_option_selected {racetype_option_selected.text}")


## Select Category
def select_category(driver, category):
	category_dropdown = wait.until(expected.element_to_be_clickable((By.CSS_SELECTOR, "[aria-owns=categories_listbox]")))
	expanded = category_dropdown.get_attribute("aria-expanded") == "true"
	if not expanded:
		category_dropdown.click()

	category_options = wait.until(expected.visibility_of_all_elements_located((By.CSS_SELECTOR, "#category_listbox li")))
	choose_element_from_list(category_options, raceType)

	category_option_selected_locator = (By.CSS_SELECTOR, "#categories_listbox li[aria-selected=true]")
	category_option_selected = driver.find_element(*category_option_selected_locator)
	print(f"category_option_selected {category_option_selected}")


## Select Season
def select_season(driver, season):
	seasons_dropdown = wait.until(expected.element_to_be_clickable((By.CSS_SELECTOR, "[aria-owns=seasons_listbox]")))
	expanded = seasons_dropdown.get_attribute("aria-expanded") == "true"
	if not expanded:
		seasons_dropdown.click()

	seasons_options = wait.until(expected.visibility_of_all_elements_located((By.CSS_SELECTOR, "#seasons_listbox li")))
	choose_element_from_list(seasons_options, raceType)

	seasons_option_selected_locator = (By.CSS_SELECTOR, "#seasons_listbox li[aria-selected=true]")
	seasons_option_selected = driver.find_element(*seasons_option_selected_locator)
	print(f"seasons_option_selected {seasons_option_selected}")

raceType = "Individual"
select_racetype(driver, raceType)

catefory = "All"
select_category(driver, raceType)

season = "2015"
select_season(driver, season)
