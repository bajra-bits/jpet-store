from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from typing import Tuple


class Register:
    # user information
    userid = (By.NAME, 'username')
    password = (By.NAME, 'password')
    repeat_password = (By.NAME, 'repeatedPassword')

    #  account information
    first_name = (By.NAME, 'account.firstName')
    last_name = (By.NAME, 'account.lastName')
    email = (By.NAME, 'account.email')
    phone = (By.NAME, 'account.phone')
    address1 = (By.NAME, 'account.address1')
    address2 = (By.NAME, 'account.address2')
    city = (By.NAME, 'account.city')
    state = (By.NAME, 'account.state')
    zip = (By.NAME, 'account.zip')
    country = (By.NAME, 'account.country')

    # preferences
    lang = (By.NAME, 'account.languagePreference',)
    category = (By.NAME, 'account.favouriteCategoryId')
    is_list = (By.NAME, 'account.listOption')
    is_banner = (By.NAME, 'account.bannerOption')

    register_btn = (By.NAME, 'newAccount')
    register_link_text = (By.LINK_TEXT, 'Register Now!')

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get_register_elements(self):
        user_list = self.userid, self.password, self.repeat_password
        information_list = (self.first_name, self.last_name, self.email,
                            self.phone, self.address1, self.address2,
                            self.city, self.state, self.zip, self.country)

        return *user_list, *information_list

    def get_lang_pref(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.lang))

    def get_category(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.category))

    def get_list(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.is_list))

    def get_banner(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.is_banner))

    def set_input_text(self, locator: Tuple[str, str], value: str):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def register(self):
        self.wait.until(EC.element_to_be_clickable(self.register_btn)).click()

    def register_link(self):
        self.wait.until(EC.element_to_be_clickable(self.register_link_text)).click()
