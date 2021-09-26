from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions

present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_located_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located
alert_present = expected.alert_is_present
text_present = expected.text_to_be_present_in_element
value_present = expected.text_to_be_present_in_element_value

# title = expected.title_is
# title_contains = expected.title_contains
# url = expected.url_to_be 
# url_changes = expected.url_changes
# url_matches = expected.url_matches
# new_window = expected.new_window_is_opened
# number_of_windows = expected.number_of_windows_to_be
# stale = expected.staleness_of

def locator(selector, by = By.CSS_SELECTOR):
	return (by, selector)

def by_id(id):
	return locator(id, By.ID),

def by_css(selector):
	return locator(selector, By.CSS_SELECTOR)

def by_xpath(xpath):
	return locator(xpath, By.XPATH)

def by_tag(tag):
	return locator(tag, By.TAG_NAME)
	
def by_link(text):
	return locator(text, By.LINK_TEXT)

def by_partial_link(text):
	return locator(text, By.PARTIAL_LINK_TEXT)


class Locate:
	
	@staticmethod
	def locator(selector, by = By.CSS_SELECTOR):
		return (by, selector)

	@staticmethod
	def by_id(id):
		return locator(id, By.ID),

	@staticmethod
	def by_css(selector):
		return locator(selector, By.CSS_SELECTOR)

	@staticmethod
	def by_xpath(xpath):
		return locator(xpath, By.XPATH)

	@staticmethod
	def by_tag(tag):
		return locator(tag, By.TAG_NAME)
		
	@staticmethod
	def by_link(text):
		return locator(text, By.LINK_TEXT)

	@staticmethod
	def by_partial_link(text):
		return locator(text, By.PARTIAL_LINK_TEXT)

