from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

expected = expected_conditions

from . import setup

present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located


def locator(selector, by = By.CSS_SELECTOR):
	return (by, selector)

def by_id(id):
	return locate,

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

class when:
	expected = expected_conditions
	present = expected.presence_of_element_located
	visible = expected.visibility_of_element_located
	clickable = expected.element_to_be_clickable
	selected = expected.element_to_be_selected
	all_present = expected.presence_of_all_elements_located
	all_visible = expected.visibility_of_all_elements_located

class locate:
	def __init__(self, locator, by=By.CSS_SELECTOR):
		self.log = setup.create_logger(__class__.__name__)
		self.log.debug(f"locate {locator} by {by}")

		self.locator = locator
		self.by = by
		
		return locator(locator, by)

	@staticmethod
	def locator(locator, by = By.CSS_SELECTOR):
		return (by, locator)

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


if __name__ == "__main__":
	print("testing utils.selenium")