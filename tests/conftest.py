import pytest

from utils import setup

@pytest.fixture
def driver():
    options = setup.get_chrome_options()
    driver = setup.get_chromedriver(chrome_options = options) 

    yield driver

    driver.quit()