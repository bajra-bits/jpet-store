import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from pageElements.login import Login


class TestLogin:
    username = '1001'
    password = 'supertest'
    base_url = 'https://petstore.octoperf.com/actions/Catalog.action'

    def test_login(self, setup):
        driver, wait = setup

        lp = Login(driver, wait)
        username_el, password_el = lp.get_login_elements()
        print(username_el, password_el)

        # get login page
        lp.login_link()
        lp.set_input_text(username_el, self.username)
        lp.set_input_text(password_el, self.password)
        lp.login()
