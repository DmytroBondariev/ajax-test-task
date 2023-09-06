from appium.webdriver.common.appiumby import AppiumBy
import subprocess
import time

import pytest
from appium import webdriver

capabilities = {
    'autoGrantPermissions': True,
    'automationName': 'uiautomator2',
    'newCommandTimeout': 500,
    'noSign': True,
    'platformName': 'Android',
    'platformVersion': '11',
    'resetKeyboard': True,
    'systemPort': 8301,
    'takesScreenshot': True,
    'udid': 'adb-0e546ef2-EPRsBh._adb-tls-connect._tcp',
    'appPackage': 'com.ajaxsystems',
    'appActivity': 'com.ajaxsystems.ui.activity.LauncherActivity'
}


class Page:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)

    def click_element(self, *args, **kwargs):
        return self.driver.click_element(*args, **kwargs)


class LoginPage(Page):
    def find_login_button(self):
        return self.find_element(AppiumBy.ACCESSIBILITY_ID, 'Log In')

    def find_email_field(self):
        return self.find_element(AppiumBy.ACCESSIBILITY_ID, 'Email')

    def find_password_field(self):
        return self.find_element(AppiumBy.ACCESSIBILITY_ID, 'Password')

    def click_login_button(self, login_button):
        login_button.click()

    def enter_email(self, email_field, email):
        email_field.send_keys(email)

    def enter_password(self, password_field, password):
        password_field.send_keys(password)


@pytest.fixture(scope='function')
def user_login_fixture(driver):
    yield LoginPage(driver)
    driver.quit()


@pytest.fixture(scope='session')
def run_appium_server():
    subprocess.Popen(
        ['appium', '-a', '0.0.0.0', '-p', '4723', '--allow-insecure', 'adb_shell'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        shell=True
    )
    time.sleep(5)


@pytest.fixture(scope='session')
def driver(run_appium_server):
    driver = webdriver.Remote('http://localhost:4723', capabilities)
    yield driver


def test_user_login(user_login_fixture):
    login_page = user_login_fixture
    login_page.click_login_button(login_page.find_login_button())
    login_page.enter_email(login_page.find_email_field(), "qa.ajax.app.automation@gmail.com")
    login_page.enter_password(login_page.find_password_field(), "qa_automation_password")
    login_page.click_login_button(login_page.find_login_button())
    assert login_page.find_element(AppiumBy.ACCESSIBILITY_ID, 'Log In') is not None
