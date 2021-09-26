import re
from typing import List
from types import SimpleNamespace

from utils import setup
from utils.file_helper import *
from utils.selenium_helper import *
from utils.WebDriverPage import WebDriverPage

# class EventResult:
	
# 	def __init__(self):
# 		self.url = None
# 		self.event_id = None
# 		self.competition_id = None
# 		self.discipline_id = None
		
# 		self.competition_name = None
# 		self.competition_url = None

# 		self.discipline = None

# 		self.details = None
# 		self.racetype = None
# 		self.venue = None
# 		self.date = None
		
# 		self.category = None

# 		self.results_excel_file = None

# 		self.table_headers = None
# 		self.table_data = None
# 		self.table_rows = None


class EventResultsFrame(WebDriverPage):

	competition_link_locator = By.CSS_SELECTOR, ".uci-main-content:nth-of-type(1) .col a"
	competition_details_locator = By.CSS_SELECTOR, ".uci-main-content:nth-of-type(1) .col span"

	export_results_link_locator = By.CSS_SELECTOR, "#exportMenu > li > .k-menu-link"
	export_to_excel_file_link_locator = By.CSS_SELECTOR, "#exportResultItem > .k-menu-link"

	results_table_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table"
	results_table_headers_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > thead > tr > th"
	results_table_rows_locator = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr"

	def __init__(self, driver:WebDriver, url:str):
		super().__init__(driver, url)
		self.log = setup.create_logger(__class__.__name__)

		self.url = url
		self.event_id = self.get_event_id()
		self.competition_id = self.get_competition_id()
		self.discipline_id = self.get_disclipline_id()

		self.event_id = None
		self.competition_id = None
		self.discipline_id = None

		self.competition_name = None
		self.competition_url = None

		self.discipline = None
		self.category = None

		self.details = None
		self.racetype = None
		self.venue = None
		self.date = None

		self.table_headers = None
		self.table_data = None
		self.table_row_data = None
	
	def open(self, url:str=None):
		super().open(url)
		
		self.url = self.driver.current_url
		self.event_id = self.get_event_id()
		self.competition_id = self.get_competition_id()
		self.discipline_id = self.get_disclipline_id()

		self.get_competition_link()
		# sets self.competition_name
		# sets self.competition_url

		self.details = self.get_competition_details()
		# sets self.details (e.g. "Individual - Venue - 15 Aug 2021 )
		# sets self.racetype 
		# sets self.venue
		# sets self.date

		return self


	def get_competition_link(self) -> WebElement:
		competition_link = self.when_clickable(self.competition_link_locator)

		self.competition_name = competition_link.text
		self.log.debug(f"got competition_name: {self.competition_name}")

		self.competition_url = competition_link.get_attribute("href")
		self.log.debug(f"got competition_url: {self.competition_url}")

		return competition_link


	def get_competition_details(self) -> WebElement:
		competition_details = self.when_visible(self.competition_details_locator)
		self.details = competition_details.text.split(" - ")
		self.log.debug(f"got details: {self.details}")

		self.racetype = self.details[0]
		self.log.debug(f"got racetype: {self.racetype}")
	
		self.venue = self.details[1]
		self.log.debug(f"got venue: {self.venue}")
	
		self.date = self.details[2]
		self.log.debug(f"got date: {self.date}")
		
		return competition_details


	def get_export_results_link(self) -> WebElement:
		export_results_link = self.when_clickable(self.export_results_link_locator)
		return export_results_link


	def get_export_to_excel_file_link(self) -> WebElement:
		export_to_excel_file_link = self.when_clickable(self.export_to_excel_file_link_locator)
		return export_to_excel_file_link


	def download_results_excel(self):
		'''
			downloads as Results.xlsx in the browser downloads directory
		'''
		self.log.debug(f"download results Excel spreadsheet to Results.xlsx")

		self.log.debug("clicking export results link to get excel file link");
		self.get_export_results_link().click()
		
		self.log.debug("clicking excel file link")
		self.get_export_to_excel_file_link().click()
		
		self.log.debug("clicked")

	def get_results_table(self) -> WebElement:
		self.when_all_present(self.results_table_headers_locator)
		results_table = self.when_visible(self.results_table_locator)
		return results_table


	def get_table_headers(self) -> List[str]:
		''' 
			returns a list of headers
			stores header text in self.table_headers
		'''
		table_headers = self.when_all_present(self.results_table_headers_locator)
		self.table_headers = [element.text for element in table_headers]
		self.log.debug(f"got table headers {self.table_headers}")
		return self.table_headers

	def get_table_data(self) -> str :
		'''
			get the raw results table data as a single block of text
			store table data in self.table_data
		'''
		results_table = self.get_results_table()
		self.table_data = results_table.text
		self.log.debug(f"got results table data {self.table_data}")
		
	def get_table_row_data(self) -> List[dict]:
		'''
			get structured table data as a list of dicts
			store table row data in self.table_row_data
			this does not go through pagination
		'''
		self.get_table_headers()
		headers = self.headers

		table_rows = self.when_all_present(self.results_table_rows_locator)
		self.log.debug(f"found {len} table_rows")

		rows = []
		for i, row in enumerate(table_rows):
			self.log.debug(f"getting data from row {i}: {row.text}")

			table_row_cells = row.find_elements_by_tag_name("td")
			
			if not len(headers) == len(table_row_cells):
				self.log.warn(f"number of headers {len(headers)} does not equal cells {len(table_row_cells)}")
				raise Exception("unable to process rows with headers")

			row = {}
			for j, cell in enumerate(table_row_cells):
				value = cell.text
				key = self.headers[j]
				self.log.debug(f"got cell value for row: {key} = {value}")
				
				row[key] = value

			self.log.debug(f"row: {row}")
			
			rows.append(row)
			self.row_data = rows
		return rows



	# https://dataride.uci.org/iframe/EventResults/253685?competitionId=65045&disciplineId=3

	@staticmethod
	def get_ids_from_event_results_url(url:str):
		match = re.search("^http.*/EventResults/(\d+).*competitionId=(\d+).*disciplineId=(\d+).*$", url)
		if match:
			return match.groups()
		else: 
			raise Exception(f"Does not look like an EventResults url : {url}")

	def get_event_id(self):
		match = re.search("^http.*/EventResults/(\d+).*$", self.url)

	def get_competition_id(self):
		match = re.search("^http.*/competitionId=/(\d+).*$", self.url)

	def get_disclipline_id(self):
		match = re.search("^http.*/disciplineId=/(\d+).*$", self.url)
