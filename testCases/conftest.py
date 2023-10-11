import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get('https://petstore.octoperf.com/actions/Catalog.action')
    driver.maximize_window()
    yield driver, wait

    time.sleep(5)
    driver.quit()
