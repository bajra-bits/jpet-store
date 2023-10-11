import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)

    driver.get('https://petstore.octoperf.com/actions/Catalog.action')
    driver.maximize_window()
    yield driver, wait

    time.sleep(10)
    driver.quit()

