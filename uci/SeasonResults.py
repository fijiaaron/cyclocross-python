from utils.selenium import *
from utils.WebDriverPage import WebDriverPage

class SeasonResultsFrame(WebDriverPage):
  
    def __init__(self, driver:WebDriver):
        super().__init__(driver)
