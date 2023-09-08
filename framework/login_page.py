from appium.webdriver.common.appiumby import AppiumBy

from .page import Page
import dev_in_test_app_team.utils.elements_xpath as xpath


class LoginPage(Page):

    def find_login_button(self):
        return self.find_element(AppiumBy.XPATH, xpath.login_button_xpath)

    def find_email_field(self):
        return self.find_element(AppiumBy.XPATH, xpath.email_field_xpath)

    def find_password_field(self):
        return self.find_element(AppiumBy.XPATH, xpath.password_field_xpath)

    @staticmethod
    def enter_email(email_field, email):
        email_field.send_keys(email)

    @staticmethod
    def enter_password(password_field, password):
        password_field.send_keys(password)
