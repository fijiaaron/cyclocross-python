from types import SimpleNamespace

class WebDriverComponent:
    
    settings = SimpleNamespace(
        timeout = 30
    )

    def __init__(self, driver, settings=None):
        self.settings = settings or self.settings
        self.logger = init_logger(__class__.__name__)
        self.driver = driver

        self.wait = WebDriverWait(driver, timeout)

    def open(self, url=None):
        self.url 
        self.driver.get(url)

        re
    def when(self, condition, locator):
        ''' 
        wait for condition 
        return element or false if not found
        '''
    