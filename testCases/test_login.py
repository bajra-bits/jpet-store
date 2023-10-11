from typing import List

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from testCases.base import BaseTest
from pageElements.login import Login
from selenium.webdriver.remote.webelement import WebElement

from testData.login_data import login_scenarios


class TestLogin(BaseTest):
    username = ''
    password = ''
    base_url = 'https://petstore.octoperf.com/actions/Catalog.action'

    @pytest.mark.parametrize("username, password", login_scenarios)
    def test_login(self, username, password, setup):
        driver, wait = setup
        lp = Login(driver, wait)
        username_el, password_el = lp.get_login_elements()

        # get login page
        lp.login_link()
        lp.set_input_text(username_el, username)
        lp.set_input_text(password_el, password)
        lp.login()

        invalid_creds: List[WebElement] = lp.get_invalid_creds()
        print(invalid_creds)
        if invalid_creds:
            for error in invalid_creds:
                print(error.text)
            return

        errors: List[WebElement] = lp.get_errors()
        if errors:
            for error in errors:
                print(error.text)
            return

        print('Login success')
