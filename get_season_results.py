lea# get_season_results.py

import os
import sys
import csv
import json

from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

# webdriver setup

expected = expected_conditions

present = expected.presence_of_element_located
visible = expected.visibility_of_element_located
clickable = expected.element_to_be_clickable
selected = expected.element_to_be_selected
all_present = expected.presence_of_all_elements_located
all_visible = expected.visibility_of_all_elements_located


def get_chrome_options(headless:bool=False, downloads:str="/tmp"):
    '''
    Get Chrome Options
    optionally run headless
    set downloads directory
    
    Args:
        headless (bool) False - Run chrome headless
        downloads (str) /tmp - Chrome downloads directory
        
    Returns:
        Options - chrome options
    '''
    
    # create chrome options
    chrome_options = Options()

    # set download directory to /tmp
    chrome_prefs = {
        "download.default_directory": downloads,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    # define headless options
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # disable images
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["download.default_directory"] = "/tmp"

    chrome_options.experimental_options["prefs"] = chrome_prefs
    
def get_chromedriver(options:Options=None):
    
    if options:
        return webdriver.Chrome(options=options)
    else:
        return webdriver.Chrome()

class SeasonResultsFrame:
    
    timeout = 30
    baseurl = "https://dataride.uci.org/"
    discipline_id = 3 # cyclocross
    path = f"iframe/results/{discipline_id}"
    url = baseurl + path 
    
    # locators
    results_table = By.CSS_SELECTOR, ".uci-table-wrapper > table"
    table_headers = By.CSS_SELECTOR, ".uci-table-wrapper > table > thead [role=columnheader]"
    table_rows = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody > tr"
    table_cells = By.CSS_SELECTOR, ".uci-table-wrapper > table > tbody [role=gridcell]"
    
    def __init__(self, webdriver:WebDriver):
        self.driver = webdriver
        self.wait = WebDriverWait(driver, SeasonResultsFrame.timeout)
    
    def open(self):
        self.driver.get(self.url)
        self.wait.until(visible(SeasonResultsFrame.results_table))
        sleep(3)
        return self
    
    def get_results_table(self) -> WebElement:
        print(f"results_table locator: {SeasonResultsFrame.results_table}")
        results_table = self.wait.until(visible(SeasonResultsFrame.results_table))
        print(f"found results_table {results_table}")
        return results_table
    
    def get_results_table_headers(self) -> List[WebElement]:
        print(f"table_headers locator: {SeasonResultsFrame.table_headers}")
        headers = self.wait.until(all_visible(SeasonResultsFrame.table_headers))
        print(f"found {len(headers)} headers")
        return headers
    
    def get_results_table_rows(self) -> List[WebElement]:
        print(f"table_rows locator: {SeasonResultsFrame.table_rows}")
        rows = self.wait.until(all_visible(SeasonResultsFrame.table_rows))
        print(f"found {len(rows)} rows")
        return rows
    
    def get_results_table_cells(self) -> List[WebElement]:
        print(f"table_cells locator: {SeasonResultsFrame.table_headers}")
        table_cells = self.wait.until(all_visible(SeasonResultsFrame.table_cells))
        print(f"foujnd {len(table_cells)} cells")
        return table_cells

if __name__ == "__main__":
    print("creating SeasonResultsFrame")
    
    try:
        chrome_options = get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        page = SeasonResultsFrame(driver).open()
        print(driver.title)
        
        table_headers = page.get_results_table_headers()
        for table_header in table_headers:
            print(table_header.text)
        
        table_rows = page.get_results_table_rows()
        for table_row in table_rows:
            print(table_row.text)
            
        table_cells = page.get_results_table_cells()
        for table_cell in table_cells:
            print(table_cell.text)
            
        results_table = page.get_results_table()
        table_body = results_table.find_element_by_tag_name("tbody")
        links = table_body.find_elements_by_tag_name("a")
        for link in links:
            url = link.get_attribute("href")
            competition = link.text
            
            print(f"link: {link.get_attribute('outerHTML')}, \
                  url: , \
                  competition: {link.text}")
            
            driver.get(link)
    finally:
        sleep(3)
        driver.quit()