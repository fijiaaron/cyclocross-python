from typing import List

from utils import setup
from utils.selenium_helper import *
from utils.WebDriverPage import WebDriverPage

class EventResultsFrame(WebDriverPage):

    heading = By.CSS_SELECTOR, ".uci-main-content:nth-of-type(1)"
    competition_link = By.CSS_SELECTOR, ".uci-main-content:nth-of-type(1) .col a"
    competition_details = By.CSS_SELECTOR, ".uci-main-content:nth-of-type(1) .col span"

    export_results_link = By.CSS_SELECTOR, "#exportMenu > li > .k-menu-link"
    export_to_excel_file_link = By.CSS_SELECTOR, "#exportResultItem > .k-menu-link"

    results_table = By.CSS_SELECTOR, ".uci-table-wrapper > table"
    results_table_headers = By.CSS_SELECTOR, ".uci-table-wrapper > table > thead > tr > th"
    results_table_rows = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr"

    def __init__(self, driver:WebDriver, url:str=None):
        super().__init__(driver, url)
        self.details = None
        self.racetype = None
        self.venue = None
        self.date = None
        self.headers = None
        self.table_data = None
        self.table_row_data = None
        
    def open(self, url:str=None):
        super().open(url)
        self.when_visible(self.results_table)
        return self

    def get_competition_link(self) -> WebElement:
        competition_link = self.when_clickable(self.competition_link)
        self.competition_name = competition_link.text
        self.log.debug(f"got competition_name: {self.competition_name}")
        self.competition_url = competition_link.get_attribute("href")
        self.log.debug(f"got competition_url: {self.competition_url}")
        return competition_link

    def get_competition_details(self) -> WebElement:
        competition_details = self.when_visible(self.competition_details)
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
        export_results_link = self.when_clickable(self.export_results_menu_link)
        return export_results_link

    def get_export_to_excel_file_link(self) -> WebElement:
        get_export_results_link = self.when_clickable(self.export_to_excel_file_link)

    def download_results_excel(self):
        '''
            downloads as Results.xlsx in the browser downloads directory
        '''
        self.log.debug(f"download results Excel spreadsheet to Results.xlsx")
        self.get_export_results_link().click()
        self.get_export_to_excel_file_link().click()

    def get_results_table(self) -> WebElement:
        self.when_all_present(self.results_table_headers)
        results_table = self.when_visible(self.results_table)
        return results_table

    def get_table_headers(self) -> List[str]:
        ''' 
            returns a list of headers
            stores header text in self.table_headers
        '''
        table_headers = self.when_all_present(self.results_table_headers)
        self.headers = [element.text for element in table_headers]
        self.log.debug(f"got table headers {self.headers}")
        return self.headers

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

        table_rows = self.when_all_present(self.results_table_rows)
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
