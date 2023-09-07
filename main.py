import sys

from appium.webdriver.common.appiumby import AppiumBy
import subprocess
import time
import pytest
from appium import webdriver
from selenium.common import NoSuchElementException
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("test_logs.log"),
                              logging.StreamHandler(sys.stdout)]
                    )

udid_command = subprocess.check_output(["adb", "devices"]).decode("utf-8")
udid = udid_command.split("\n")[1].split("\t")[0]

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
    'udid': udid,
    'appPackage': 'com.ajaxsystems',
    'appActivity': 'com.ajaxsystems.ui.activity.LauncherActivity'
}


class Page:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)

    @staticmethod
    def click_element(element):
        element.click()


class LoginPage(Page):

    def find_login_button(self):
        return self.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Log In"]')

    def find_email_field(self):
        xpath_locator = '//android.widget.FrameLayout[1]/androidx.compose.ui.platform.ComposeView/' \
                        'android.view.View/android.widget.EditText'
        return self.find_element(AppiumBy.XPATH, xpath_locator)

    def find_password_field(self):
        xpath_locator = "//android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/" \
                        "android.view.View/android.widget.EditText"
        return self.find_element(AppiumBy.XPATH, xpath_locator)

    @staticmethod
    def enter_email(email_field, email):
        email_field.send_keys(email)

    @staticmethod
    def enter_password(password_field, password):
        password_field.send_keys(password)


@pytest.fixture(scope='function', autouse=True)
def user_login_fixture(driver):
    logging.info("Setting up user_login_fixture")

    yield LoginPage(driver)
    logging.info("Tearing down user_login_fixture")


@pytest.fixture(scope='session')
def run_appium_server():
    subprocess.Popen(
        ['appium', '-a', '0.0.0.0', '-p', '4723', '--allow-insecure', 'adb_shell'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        shell=True
    )
    time.sleep(3)


@pytest.fixture(scope='function')
def driver(run_appium_server):
    logging.info("Setting up driver fixture")

    driver = webdriver.Remote('http://localhost:4723', capabilities)
    yield driver
    logging.info("Tearing down driver fixture")
    driver.quit()


def assert_login_successful(login_page):
    assert login_page.find_element(AppiumBy.XPATH,
                                   "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                   "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                   "androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/"
                                   "android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup/"
                                   "android.widget.FrameLayout/android.widget.ImageView") is not None


def assert_login_failed(login_page):
    with pytest.raises(NoSuchElementException):
        login_page.find_element(AppiumBy.XPATH,
                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                "androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/"
                                "android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup/"
                                "android.widget.FrameLayout/android.widget.ImageView")


@pytest.mark.parametrize("email, password, expected_result", [
    ("qa.ajax.app.automation@gmail.com", "qa_automation_password", "success"),
    ("invalid_email@example.com", "qa_automation_password", "failure"),
    ("qa.ajax.app.automation@gmail.com", "invalid_password", "failure"),
    ("qa.ajax.app.automation@gmail.com", "  ", "failure"),
    ("  ", "qa_automation_password", "failure"),
])
def test_user_login(user_login_fixture, email, password, expected_result):
    login_page = user_login_fixture
    logging.info(f"Logging in with email: {email} and password: {password}")

    login_page.click_element(login_page.find_login_button())
    login_page.enter_email(login_page.find_email_field(), email)
    login_page.enter_password(login_page.find_password_field(), password)
    login_page.click_element(login_page.find_login_button())

    logging.info("Waiting for 3 seconds after clicking login button.")

    time.sleep(3)

    if expected_result == "success":
        logging.info("Login successful. Asserting success.")

        assert_login_successful(login_page)
    elif expected_result == "failure":
        logging.info("Login expected to fail. Asserting failure.")

        assert_login_failed(login_page)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'main.py'])
