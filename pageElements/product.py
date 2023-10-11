import time
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Product:
    sidebar = (By.XPATH, "//div[@id='SidebarContent']")
    table = (By.XPATH, "//tbody")
    prod_link = (By.XPATH, "//a")
    add_to_cart_btn = (By.XPATH, "//a[@class='Button' and contains(text(), 'Cart')]")
    cart_btn = (By.XPATH, "//img[@name='img_cart']")
    proceed_to_checkout_btn = (By.XPATH, "//a[@class='Button' and contains(text(), 'Checkout')]")
    continue_btn = (By.XPATH, "//input[@type='submit' and @name='newOrder']",)
    confirm_btn = (By.XPATH, "//a[@class='Button' and contains(text(), 'Confirm')]",)
    confirmation_text = (By.XPATH, "//ul[@class='messages']//li")
    main_menu_btn = (By.XPATH, "//div[@id='BackLink']//*[contains(text(), 'Main Menu')]")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def pick_product(self, prod: str):

        sidebar: WebElement = self.wait.until(EC.visibility_of_element_located(self.sidebar))

        target_link: WebElement = sidebar.find_element(By.XPATH, f"//a[contains(@href, '{prod.upper()}')]")
        target_link.click()

        # product table
        product_table: WebElement = self.wait.until(EC.visibility_of_element_located(self.table))
        product_list: List[WebElement] = product_table.find_elements(By.XPATH,
                                                                     ".//a[contains(@href, '/actions')]")

        for product in product_list:
            product.click()

            # items table
            item_table: WebElement = self.wait.until(EC.visibility_of_element_located(self.table))
            item_list: List[WebElement] = item_table.find_elements(By.XPATH, "//table//a[not(@class='Button')]")

            for item in item_list:
                item.click()
                self.wait.until(EC.element_to_be_clickable(self.add_to_cart_btn)).click()
                self.driver.back()
                self.driver.back()

            self.driver.back()

        self.driver.back()

    def cart_icon_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.cart_btn)).click()

    def display_cart_items(self):
        cart_table: WebElement = self.wait.until(EC.visibility_of_element_located(self.table))
        items_list: List[WebElement] = cart_table.find_elements(By.XPATH, '//tr')

        selected_items = items_list[1:len(items_list) - 1]

        for item in selected_items:
            prod_id = item.find_element(By.XPATH, "./td[2]")
            desc = item.find_element(By.XPATH, "./td[3]")
            rate = item.find_element(By.XPATH, "./td[6]")

            print("***** Cart Item Details *****")
            print(f"ProductID: {prod_id.text}")
            print(f"Description: {desc.text}")
            print(f"Rate: {rate.text}")

        print(f"Total items in cart: {len(selected_items)}")

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.proceed_to_checkout_btn)).click()
        self.wait.until(EC.element_to_be_clickable(self.continue_btn)).click()
        self.wait.until(EC.element_to_be_clickable(self.confirm_btn)).click()

    def get_confirmation_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.confirmation_text)).text

    def main_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.main_menu_btn)).click()
