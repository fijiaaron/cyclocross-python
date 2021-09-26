import re

from utils import setup
from utils.selenium_helper import *
from utils.WebDriverPage import WebDriverPage

class SeasonResultsFrame(WebDriverPage):

	url = "https://dataride.uci.org/iframe/results/3"

	results_heading_selector = (By.CSS_SELECTOR, ".uci-label")

	racetype_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=raceTypes_listbox] [class*=arrow]")
	racetype_dropdown_selector = (By.CSS_SELECTOR, "#raceTypes")
	racetype_options_selector = (By.CSS_SELECTOR, "#raceTypes_listbox li")
	racetype_option_selected = (By.CSS_SELECTOR, "#raceTypes_listbox li[aria-selected=true]")

	category_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=categories_listbox] [class*=arrow]")
	category_dropdown_selector = (By.CSS_SELECTOR, "#categories")
	category_options_selector = (By.CSS_SELECTOR, "#categories_listbox li")
	category_option_selected = (By.CSS_SELECTOR, "#categories_listbox li[aria-selected=true]")

	season_dropdown_arrow_selector = (By.CSS_SELECTOR, "[aria-owns=seasons_listbox] [class*=arrow]")
	season_dropdown_selector = (By.CSS_SELECTOR, "#seasons")
	season_options_selector = (By.CSS_SELECTOR, "#seasons_listbox li")
	season_option_selected = (By.CSS_SELECTOR, "#seasons_listbox li[aria-selected=true]")

	date_table_header_selector = (By.CSS_SELECTOR, "[data-title=Date]")
	competition_table_header_selector = (By.CSS_SELECTOR, "[data-title=Competition]")
	country_table_header_selector = (By.CSS_SELECTOR, "[data-title=Country]")
	class_table_header_selector = (By.CSS_SELECTOR, "[data-title=Class]")

	loading_selector = (By.CSS_SELECTOR, ".k-loading-mask")
	competition_table_row_selector = (By.CSS_SELECTOR, "#competitions table tbody tr")
	
	next_page_selector = (By.CSS_SELECTOR, '[title="Go to the next page"]')
	prev_page_selector = (By.CSS_SELECTOR, '[title="Go to the previous page"]')
	current_page = (By.CSS_SELECTOR, ".k-pager-numbers .k-state-selected")

	def __init__(self, driver:WebDriver):
		super().__init__(driver, SeasonResultsFrame.url)
		self.log = setup.create_logger(__class__.__name__)
		self.racetype = None
		self.category = None
		self.season = None

	def open(self, url=None):
		super().open()

		self.log.debug(f"got title: {self.driver.title}")
		heading = self.wait.until(visible(self.results_heading_selector))
		self.log.debug(f"results_heading: {heading.text}")


	def choose_element_from_list(self, elements, matcher) -> WebElement:
		self.log.debug(f"{len(elements)} elements matcher: {matcher}")
		for element in elements:
			self.log.debug(f"element.txt: {element.text}")
			if element.text == matcher:
				return element
			else:
				self.log.warn("no match found")
		# return next(filter(lambda element: element.text == matcher, elements))


	def wait_for_loading_to_clear(self):
		self.log.debug(f"wait for loading mask to indicate refreshed data")
		quickwait = WebDriverWait(self.driver, 3)
		try:
			quickwait.until(expected.visibility_of_element_located(self.loading_selector))
		except WebDriverException:
			self.log.debug("loading not present")
		finally:
			self.wait.until_not(expected.presence_of_element_located(self.loading_selector))
		

	def select_racetype(self, racetype="All", forceSelection=False):
		self.log.debug(f"select racetype: {racetype}")
		self.racetype = racetype
	
		if racetype == "All" and not forceSelection:
			self.log.debug("doing nothing - default racetype should be selected")
			return

		racetype_dropdown = self.when_clickable(self.racetype_dropdown_arrow_selector)

		self.log.debug(f"click racetype_dropdown: {racetype_dropdown}")
		racetype_dropdown.click()

		racetype_options = self.when_all_visible(self.racetype_options_selector)
		
		self.log.debug(f"choose racetype from racetype_options: {racetype_options}")
		self.choose_element_from_list(racetype_options, racetype).click()

		self.wait_for_loading_to_clear()
		

	def select_category(self, category="All", forceSelection=False):
		self.log.debug(f"select_category({category}")
		self.category = category

		if category == "All" and not forceSelection:
			self.log.debug("doing nothing - default category should be selected")
			return 

		category_dropdown = self.when_clickable(self.category_dropdown_arrow_selector)

		self.log.debug(f"click category dropdown: {category_dropdown}")
		category_dropdown.click()

		category_options = self.when_all_visible(self.category_options_selector)

		self.log.debug(f"choose category from category_options: {category_options}")
		self.choose_element_from_list(category_options, category).click()

		self.wait_for_loading_to_clear()


	def select_season(self, season="current", forceSelection=False):
		self.log.debug(f"select_season({season})")
		self.season = season

		if season == "current" and not forceSelection:
			self.log.debug("doing nothing - default season should be selected")
			return

		self.log.debug(f"waiting for element to be clickable {self.season_dropdown_arrow_selector}")
		season_dropdown = self.when_clickable(self.season_dropdown_arrow_selector)

		self.log.debug(f"click season dropdown {season_dropdown}")
		season_dropdown.click()

		season_options = self.when_all_visible(self.season_options_selector)

		self.log.debug(f"choose season from season_options: len({season_options})")
		self.choose_element_from_list(season_options, season).click()

		self.wait_for_loading_to_clear()


	def get_results(self):
		rows = self.when_all_visible(self.competition_table_row_selector)
		self.log.debug(f"total rows: {len(rows)}")

		competitions = []

		for row in rows:
			cells:List[WebElement] = row.find_elements(By.TAG_NAME, "td")
			
			competition_url = cells[1].find_element(By.TAG_NAME, "a").get_attribute("href")

			competition = {
				"date" : cells[0].text,
				"name" : cells[1].text,
				"country_code" : cells[2].text,
				"competition_class" : cells[3].text,
				"race_type" : self.racetype,
				"category" : self.category,
				"season" : self.season,
				"discipline": "Cyclo-cross",
				"discipline_id": 3,
				"id" : self.get_competition_id_from_url(competition_url),
				"url" : competition_url,
			}
			
			self.log.debug(f"competition: {competition}")
			competitions.append(competition)

		self.log.debug(f"total competitions: {len(competitions)}")
		return competitions


	def get_current_page_number(self):
		current_page = self.wait.until(present(self.current_page))
		return int(current_page.text)

	def go_to_next_page(self):
		next_page = self.wait.until(present(self.next_page_selector))
		disabled = 'disabled' in next_page.get_attribute("class")
 
		if disabled:
			return False
		else: 
			next_page.click()


	def has_next_page(self):
		next_page = self.wait.until(present(self.next_page_selector))
		disabled = 'disabled' in next_page.get_attribute("class")
		if disabled:
			return False
		else:
			return True


	def go_to_previous_page(self):
		previous_page = self.wait.until(present(self.prev_page_selector))
		disabled = 'disabled' in previous_page.get_attribute("class")
		if disabled:
			 return False
		previous_page.click()


	@staticmethod
	def get_competition_id_from_url(url):
		match = re.search("^http.*/CompetitionResults/(\d+).*$", url)

		if match and match.groups() and len(match.groups()) == 1:
			return match.groups()[0]
		else:
			raise Exception("URL does not look like CompetitionResults: {url}")
