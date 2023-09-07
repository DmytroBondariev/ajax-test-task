from appium.webdriver.common.appiumby import AppiumBy
import subprocess
import time
import pytest
from appium import webdriver
from selenium.common import NoSuchElementException

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
    yield LoginPage(driver)


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
    driver = webdriver.Remote('http://localhost:4723', capabilities)
    yield driver
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
    login_page.click_element(login_page.find_login_button())
    login_page.enter_email(login_page.find_email_field(), email)
    login_page.enter_password(login_page.find_password_field(), password)
    login_page.click_element(login_page.find_login_button())
    time.sleep(3)

    if expected_result == "success":
        assert_login_successful(login_page)
    elif expected_result == "failure":
        assert_login_failed(login_page)
