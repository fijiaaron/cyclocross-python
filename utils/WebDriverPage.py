from typing import List

from utils.selenium_helper import *
from utils import setup


class WebDriverPage(object):

	def __init__(self, driver:WebDriver, url=None, timeout=30):
		self.log = setup.create_logger(__class__.__name__)
		self.log.debug(f"initialized with driver {driver}")
		self.driver = driver
		self.url = url
		self.timeout = timeout
		self.wait = WebDriverWait(self.driver, self.timeout)

	def open(self, url=None):
		if url:
			self.url = url
		if  self.url:
			self.log.debug(f"open {self.url}")
			self.driver.get(self.url)
			return self
		else:
			self.log.warn(f"no url to open")
		   
	def when_present(self, locator:tuple, description="element") -> WebElement:
		self.log.debug(f"wait until {description} present {locator}")
		try:
			element = self.wait.until(present(locator))
			self.log.debug(f"found {description} {element}")
			return element
		except WebDriverException as e:
			self.log.warning("f{description} not found {locator}")
			raise e
	   
	def when_all_present(self, locator:tuple, description="elements") -> List[WebElement]:
		self.log.debug(f"wait until {description} all present {locator}")
		try:
			elements = self.wait.until(all_present(locator))
			self.log.debug(f"found {len(elements)} {description}")
			return elements
		except WebDriverException as e:
			self.log.warning(f"{description} not found {locator}")
			raise e
		
	def when_visible(self, locator:tuple, description="element") -> WebElement:
		self.log.debug(f"wait until {description} visible {locator}")
		try: 
			element = self.wait.until(visible(locator))
			self.log.debug(f"found {description} {element}")
			return element
		except WebDriverException as e:
			self.log.warning(f"{description} not found {locator}")
			raise e
			
	def when_all_visible(self, locator:tuple, description="elements") -> List[WebElement]:
		self.log.debug(f"wait until {description}  all visible {locator}")
		try: 
			elements = self.wait.until(all_visible(locator))
			self.log.debug(f"found {len(elements)} description")
			return elements
		except WebDriverException as e:
			self.log.warning(f"{description} not found {locator}")
			raise e

	def when_clickable(self, locator:tuple, description="element") -> WebElement:
		self.log.debug(f"wait until {description} clickable {locator}")
		try:
			element = self.wait.until(clickable)
			self.log.debug(f"found {description} {element}")
			return element
		except WebDriverException as e:
			self.log.warning(f"{description} not found {locator}")
			raise e

	def when_selected(self, locator:tuple, description="element") -> WebElement:
		self.log.debug(f"wait until {description} selected {locator}")
		try:
			element = self.wait.until(selected(locator))
			self.log.debug(f"found {description} {element}")
			return element
		except WebDriverException as e:
			self.log.warning(f"{description} not found {locator}")
			raise e

	
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
		