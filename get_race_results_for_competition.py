import setup

from selenium import webdriver

from uci.cyclocross.CompetitionResultsFrame import CompetitionResultsFrame
from uci.cyclocross.Competition import Competition

competition_url="https://dataride.uci.org/iframe/CompetitionResults/65045?disciplineId=3"

log = setup.create_logger(__name__)
driver = webdriver.Chrome()

page = CompetitionResultsFrame(driver, url=competition_url)
page.open()
print(page.competition)
print(page.competition.to_json())

