import re 
from time import sleep 
from typing import List
from types import SimpleNamespace

from utils import setup
from utils.selenium_helper import *
from utils.WebDriverPage import WebDriverPage

class CompetitionResultsFrame(WebDriverPage):

	results_link_locator = By.LINK_TEXT, "Results"

	competition_name_locator = By.CSS_SELECTOR , ".uci-label"

	competition_details_locator    = By.CSS_SELECTOR, "ul.uci-detail-list li"
	competition_discipline_locator = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(1)"
	competition_dates_locator      = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(2)"
	competition_class_locator      = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(3)"
	competition_venue_locator      = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(4)"
	competition_country_locator    = By.CSS_SELECTOR, "ul.uci-detail-list li:nth-of-type(5)"

	results_table_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table"
	table_headers_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > thead [role=columnheader]"
	table_body_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody"
	table_row_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr[role=row]"

	general_classification_link_locator = By.LINK_TEXT, "General Classification"

	main_rows_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-master-row"
	detail_rows_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-detail-row"

	collapse_icons_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody [aria-label=Collapse]"
	expand_icons_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody [aria-label=Expand]"

	categories_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr.k-master-row > td:last-of-type"

	def __init__(self, driver:WebDriver, url:str):
		super().__init__(driver, url)
		self.log = setup.create_logger(__class__.__name__)
		self.log.debug("init")

		if url:
			self.url = url

		self.competition_id = self.get_competition_id_from_url(url)
		self.discpline_id = self.get_discipline_id_from_url(url)

		self.season_results_url = None
		self.competition_name = None
		self.competition_url = self.url
		
		self.competition_discipline = None
		self.competition_dates = None
		self.competition_class = None
		self.competition_venue = None
		self.competition_country = None

		self.categories = None
		self.events = None

		self.race_name = None
		self.race_date = None
		self.race_venue = None
		self.race_category = None


	def open(self, url:str=None):
		self.log.debug(f"open url: {url}")
		if url:
			self.url = url

		super().open(self.url)
	
		url = self.driver.current_url
		self.competition_id = self.get_competition_id_from_url(url)
		self.discpline_id = self.get_discipline_id_from_url(url)
	
		self.season_results_url = self.get_season_results_url()

		self.competition_name = self.get_competition_name()
		self.competition_discipline = self.get_competition_discipline()
		self.competition_dates = self.get_competition_dates()
		self.competition_class = self.get_competition_class()
		self.competition_venue = self.get_competition_venue()
		self.competition_country = self.get_competition_country()

		self.categories = self.get_categories()
		self.table_headers = self.get_table_headers()
		

	def get_season_results_url(self):
		results_link = self.when_clickable(self.results_link_locator, "season_results")
		season_results_url = results_link.get_attribute("href")
		self.log.debug(f"got season_results_url: {season_results_url}")
		return season_results_url


	def get_competition_name(self):
		competition_name = self.when_visible(self.competition_name_locator, "competition_name").text
		self.log.debug(f"got competition_name: {competition_name}")
		return competition_name


	def get_competition_discipline(self):
		competition_discipline = self.when_visible(self.competition_discipline_locator, "competition_locator").text
		self.log.info(f"got competition_discipline: {competition_discipline}")
		return competition_discipline


	def get_competition_dates(self):
		competition_dates = self.when_visible(self.competition_dates_locator, "competition_dates").text
		self.log.info(f"got competition_dates: {competition_dates}")
		return competition_dates


	def get_competition_class(self):
		competition_class = self.when_visible(self.competition_class_locator, "competition_class").text
		self.log.info(f"got competition_class: {competition_class}")
		return competition_class


	def get_competition_venue(self):
		competition_venue = self.when_visible(self.competition_venue_locator, "competition_venue").text
		self.log.info(f"got competition_venue: {competition_venue}")
		return competition_venue


	def get_competition_country(self):
		competition_country = self.when_visible(self.competition_country_locator, "competition_country").text
		self.log.info(f"got competition_country: {competition_country}")
		return competition_country


	def get_table_headers(self):
		table_headers_elements = self.when_all_visible(self.table_headers_locator, "table_headers")
		table_headers = [header.text for header in table_headers_elements]
		self.log.debug(f"got table_headers: {table_headers}")
		return table_headers 


	def get_categories(self):
		category_elements = self.when_all_visible(self.categories_locator)
		categories = [category_element.text for category_element in category_elements]
		self.log.debug(f"got categories: {categories}") 
		return categories


	def get_event_results(self):
		table_rows_elements = self.when_all_present(self.table_row_locator, "table_rows")
		rows_text = [row.text for row in table_rows_elements]
		self.log.debug(f"got rows_text: {rows_text} ")

		self.collapse_all_rows()
		self.expand_all_rows()

		main_rows = self.when_all_visible(self.main_rows_locator)
		detail_rows = self.when_all_visible(self.detail_rows_locator)
		
		events = []
		for index, main_row in enumerate(main_rows):
			
			event = SimpleNamespace()
			event.competition_url = self.url
			event.competition_id = self.competition_id
			event.competition_name = self.competition_name
			event.discipline_id = self.discpline_id
			event.discipline = self.competition_discipline
			event.competition_dates = self.competition_dates
			event.competition_class = self.competition_class
			event.competition_venue = self.competition_venue
			event.competition_country = self.competition_country
			
			# get data from row
			event.name = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)").text # this row actually has the category
			event.date = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)").text
			event.venue = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(4)").text
			event.category = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(5)").text
			self.log.debug(f"got row {index} {event.name}, {event.date}, {event.venue}, {event.category}")
			
			# get arrow to expand row
			arrow = main_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(1) a")
			arrow_label = arrow.get_attribute("aria-label")
			self.log.debug(f"row {index} arrow_label: {arrow_label}")

			### This may be needed to expand if expand_all_rows() didn't work
			if arrow_label == "Expand":
				log.debug("clicking 'Expand' arrow for row {index}")
				arrow.click()
				sleep(5)

			# find detail row relative to main row
			##replaced## detail_row = main_row.find_element(By.XPATH, "./following-sibling::tr[1]")
			detail_row_locator = By.XPATH, "./following-sibling::tr[contains(@class, 'k-detail-row')]"
			detail_row = self.wait_in(main_row).until(visible(detail_row_locator))
			
			# get event link from detail row
			## replaced ## link = detail_row.find_element_by_tag_name("a")
			event_link_locator = By.TAG_NAME, "a"
			event_link = self.wait_in(detail_row).until(clickable(event_link_locator))
			
			# get event url from event link
			event.url = event_link.get_attribute("href")
			self.log.debug(f"got event_url: {event.url}")
		
			# get event winner
			event.winner = detail_row.find_element(By.XPATH, "//td[2]").text
			self.log.debug(f"got winner {event.winner}")
			
			# convert event to a dict before adding to list
			events.append(event.__dict__) 

		self.log.debug(f"got {len(events)} events")
		return events
	

	def expand_all_rows(self):
		self.log.debug(f"expand_all_rows()")
		try:
			expand_links = self.when_all_visible(self.expand_icons_locator)
			self.log.debug(f"expanding {len(expand_links)} rows")
			for link in expand_links:
				link.click()
				sleep(2)
		except TimeoutException as e:
			self.log.debug(f"no rows to expand")
		
		sleep(5)
		event_links = self.when_all_visible(self.general_classification_link_locator, "event_links")
		self.log.debug(f"got {len(event_links)} event links")


	def collapse_all_rows(self):
		self.log.debug(f"collapse_all_rows")
		
		try:
			collapse_links = self.when_all_visible(self.collapse_icons_locator)
			self.log.debug(f"collapsing {len(collapse_links)} rows")
			for link in collapse_links:
				link.click()
				sleep(2)
		except TimeoutException as e:
			self.log.debug(f"no rows to collapse")


	@staticmethod
	def get_competition_id_from_url(url:str):
		match = re.search("^http.*/CompetitionResults/(\d+).*$", url)
		if match and len(match.groups()) == 1:
			competition_id = match.groups()[0]
			return competition_id
		
		raise Exception("URL does not look like CompetitionResults: {url}")


	@staticmethod
	def get_discipline_id_from_url(url:str):
		if "disciplineId" in url:
			match = re.search("^http.*disciplineId=(\d+).*$", url)
			if match and len(match.groups()) == 1:
				discipline_id = match.groups()[0]
				return discipline_id
			else:
				raise Exception(f"Does not look like a CompetitionResults url {url}")
		else:
			match = re.search("^http.*/CompetitionResults/(\d+)/(\d+).*$", url)
			if match and len(match.groups()) == 2:
				discipline_id = match.groups()[1]
				return discipline_id

		raise Exception(f"URL does not look like CompetitionResults: {url}")
