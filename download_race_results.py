from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
expected = expected_conditions
clickable = expected.element_to_be_clickable

race_results_url = "https://dataride.uci.org/iframe/EventResults/253649/65009/3"

export_results_menu_locator = By.CSS_SELECTOR, "#exportMenu"
export_to_excel_file_locator = By.CSS_SELECTOR, "#exportResultItem"
competition_link_locator = By.CSS_SELECTOR, "#event-results-view .uci-main-content:first-of-type a"

def click(locator):
	print(f"click({locator})")
	print(f"wait until clickable {locator}")
	element = wait.until(clickable(locator))
	print("click element: {element}")
	element.click()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

# open race results frame
driver.get(race_results_url)

# get competition info
competition_link = wait.until(clickable(*competition_link_locator))
competition_name = competition_link.text
competition_url = competition_link.get_attribute("href")

element = wait.until(clickable(competition_link))
# download spreadsheet
wait.until(clickable(export_results_menu_locator)).click()
wait.until(clickable(export_to_excel_file_locator)).click()
