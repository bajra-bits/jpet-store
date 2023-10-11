import pytest
from typing import List


from pageElements.login import Login
from selenium.webdriver.remote.webelement import WebElement

from testData.login_data import login_scenarios


@pytest.mark.parametrize("username, password", login_scenarios)
def test_login(username, password, setup):
    driver, wait = setup
    lp = Login(driver, wait)
    username_el, password_el = lp.get_login_elements()

    # get login page
    lp.login_link()
    lp.set_input_text(username_el, username)
    lp.set_input_text(password_el, password)
    lp.login()

    # check for invalid creds
    invalid_creds: List[WebElement] = lp.get_invalid_creds()
    print(invalid_creds)
    if invalid_creds:
        for error in invalid_creds:
            print(error.text)
        return

    # check for field errors
    errors: List[WebElement] = lp.get_errors()
    if errors:
        for error in errors:
            print(error.text)
        return

    print('***** LOGIN SUCCESS *****')
    lp.logout()
