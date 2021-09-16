
import setup
from uci.cyclocross.results import CyclocrossResults

log = setup.create_log()
driver = setup.create_chromedrover()

results = CyclocrossResults(driver).open()

results.set_raceType("All")
results.set_category("All")
results.set_season("2022")

results.wait_for_change()

