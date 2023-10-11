from typing import List, Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Login:
    username = (By.NAME, "username")
    password = (By.NAME, "password")
    login_btn = (By.NAME, "signon")
    login_link_text = (By.LINK_TEXT, "Sign In")
    logout_link_text = (By.LINK_TEXT, "Sign Out")
    errors = (By.XPATH, "//div[@id='Catalog']//*[contains(text(), 'Please enter your username and password.')]")
    invalid_creds = (By.XPATH, "//ul[@class='messages']//*[contains(text(), 'Signon failed')]")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get_errors(self) -> List[WebElement]:
        return self.driver.find_elements(*self.errors)

    def get_invalid_creds(self):
        return self.driver.find_elements(*self.invalid_creds)

    def get_login_elements(self):
        return self.username, self.password

    def set_input_text(self, locator: Tuple[str, str], value: str):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def login(self):
        self.wait.until(EC.element_to_be_clickable(self.login_btn)).click()

    def login_link(self):
        self.wait.until(EC.element_to_be_clickable(self.login_link_text)).click()

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_link_text)).click()
