import os
import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv
from selenium.common import NoSuchElementException

import dev_in_test_app_team.utils.elements_xpath as xpath

load_dotenv()


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
    (os.getenv("TEST_EMAIL"), os.getenv("TEST_PASSWORD"), "success"),
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

    time.sleep(4)

    if expected_result == "success":

        assert_login_successful(login_page)
    elif expected_result == "failure":

        assert_login_failed(login_page)
