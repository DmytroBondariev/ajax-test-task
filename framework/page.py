class Page:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self):
        raise NotImplementedError

    def click_element(self):
        raise NotImplementedError
