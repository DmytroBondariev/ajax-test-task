class Page:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)

    @staticmethod
    def click_element(element):
        element.click()
