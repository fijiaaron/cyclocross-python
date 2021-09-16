import setup
from typing import List

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


class Locator():
	def __init__(self, driver):
		self.driver = driver
		self.log = setup.create_logger(__class__.__name__)

	def create(self, text, strategy=By.CSS_SELECTOR, timeout=None, description=None):
		self.log(f"create {text} by {strategy} with timeout {timeout} and description {description}")
		instance = Locator(text=text, strategy=strategy, timeout=timeout, description=description)
		return instance

	def present(self, locator, strategy=By.CSS_SELECTOR, timeout=0, description=None):
		self.locator = locator
		self.by = strategy
		self.timeout = timeout
		self.log = setup.create_logger(__class__.__name__)

	def whenVisible(self, locator, strategy=By.CSS_SELECTOR, timeout=0, description=None):
		self.locator = locator
		self.by = strategy
		self.timeout = timeout
		self.log = setup.create_logger(__class__.__name__)

	def get(self):
		return self.by, self.locator

	def find(self, driver:WebDriver=None, timeout=None) -> WebElement:
		if timeout:
			wait = WebDriverWait(driver, timeout)
			return wait.until(visible(self.get()))
		else:
			return driver.find_element(self.get())

	def click(self, driver=None, timeout=None):
		if timeout:
			wait = WebDriverWait(driver, timeout)
			return wait.until(clickable(self.get()))

		else:
			driver.find
