import sys

from appium.webdriver.common.appiumby import AppiumBy
import subprocess
import time
import pytest
from appium import webdriver
from selenium.common import NoSuchElementException
import logging

import utils.elements_xpath as xpath
from dev_in_test_app_team.framework import LoginPage
from utils.android_utils import android_get_desired_capabilities

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("test_logs.log"),
                              logging.StreamHandler(sys.stdout)]
                    )


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
    time.sleep(5)


@pytest.fixture(scope='function')
def driver(run_appium_server):
    logging.info("Setting up driver fixture")

    driver = webdriver.Remote('http://localhost:4723', android_get_desired_capabilities())
    yield driver
    logging.info("Tearing down driver fixture")
    driver.quit()


def assert_login_successful(login_page):
    assert login_page.find_element(
        AppiumBy.XPATH,
        xpath.burger_menu_xpath
    ) is not None


def assert_login_failed(login_page):
    with pytest.raises(NoSuchElementException):
        login_page.find_element(
            AppiumBy.XPATH,
            xpath.burger_menu_xpath
        )


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

    time.sleep(4)

    if expected_result == "success":
        logging.info("Login successful. Asserting success.")

        assert_login_successful(login_page)
    elif expected_result == "failure":
        logging.info("Login expected to fail. Asserting failure.")

        assert_login_failed(login_page)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'main.py'])
