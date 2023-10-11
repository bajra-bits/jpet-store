from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Login:
    username = (By.NAME, 'username')
    password = (By.NAME, 'password')
    login_btn = (By.NAME, 'signon')
    login_link_text = (By.LINK_TEXT, 'Sign In')
    logout_link_text = (By.LINK_TEXT, 'Sign Out')

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get_login_elements(self):
        return self.username, self.password

    def set_input_text(self, locator, value):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def login(self):
        self.wait.until(EC.element_to_be_clickable(self.login_btn)).click()

    def login_link(self):
        self.wait.until(EC.element_to_be_clickable(self.login_link_text)).click()

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_link_text)).click()
