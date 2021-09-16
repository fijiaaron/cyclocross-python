import setup

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected

class UCIPage(object):

	__TIMEOUT = 15

	_URL = "https://www.uci.org"
	_TITLE = ""


	def __init__(self, driver:WebDriver):
		self.driver = driver
		self.wait = WebDriverWait(driver, self.__TIMEOUT)
		self.log = setup.create_logger(self.__class__.__name__)

	def open(self):
		self.driver.get(self.url)


