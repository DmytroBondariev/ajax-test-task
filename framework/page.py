class Page:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *args, **kwargs):
        raise self.driver.find_element(*args, **kwargs)

    def click_element(self, *args, **kwargs):
        return self.driver.click_element(*args, **kwargs)
