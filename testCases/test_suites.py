import pytest
from typing import List

from selenium.webdriver.support.select import Select

from pageElements.login import Login
from selenium.webdriver.remote.webelement import WebElement

from pageElements.product import Product
from pageElements.register import Register
from testData.login_data import login_scenarios
from testData.product_data import products_scenario
from testData.register_data import register_scenario
from utils.variables import DEFAULT_LANG, DEFAULT_CATEGORY, DUPLICATE_USER, REGISTER_URI, CONFIRMATION_TEXT


@pytest.mark.parametrize("dataset", register_scenario)
def test_register(dataset, setup):
    driver, wait = setup
    lp = Login(driver, wait)
    rp = Register(driver, wait)

    # get register page
    lp.login_link()
    rp.register_link()

    rp_elements = rp.get_register_elements()
    for locator in rp_elements:
        loc_type, identifier = locator
        rp.set_input_text(locator, dataset[identifier])

    # Get dropdowns
    lang_dropdown = rp.get_lang_pref()
    cat_dropdown = rp.get_category()

    # Create a Select object
    lang_select = Select(lang_dropdown)
    cat_select = Select(cat_dropdown)

    lang_pref_value: str = dataset['account.languagePreference']
    lang_pref_value = DEFAULT_LANG if len(lang_pref_value.strip()) < 1 else lang_pref_value

    cat_pref_value = dataset['account.favouriteCategoryId']
    cat_pref_value = DEFAULT_CATEGORY if len(cat_pref_value.strip()) < 1 else cat_pref_value
    lang_select.select_by_value(lang_pref_value.lower())
    cat_select.select_by_value(cat_pref_value.upper())

    # Get radio buttons
    my_list = rp.get_list()
    my_banner = rp.get_banner()

    my_list_enable: bool = dataset['account.listOption']
    my_banner_enable: bool = dataset['account.bannerOption']

    if my_list_enable:
        if not my_list.is_enabled():
            my_list.click()

    else:
        if my_list.is_enabled():
            my_list.click()

    if my_banner_enable:
        if not my_banner.is_enabled():
            my_banner.click()

    else:
        if my_banner.is_enabled():
            my_banner.click()

    rp.register()

    if DUPLICATE_USER in driver.title:
        print("***** DUPLICATE USER *****")
        driver.back()
        return

    if REGISTER_URI in driver.current_url:
        print('***** NOT REGISTERED. INPUT AGAIN ******')
        return

    print('******** USER REGISTERED *******')


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
    # lp.logout()


@pytest.mark.parametrize("products", products_scenario)
def test_pick_products(products, setup):
    print(products)
    driver, wait = setup
    pp = Product(driver, wait)

    # add items to cart
    for product in products:
        pp.pick_product(product)

    pp.cart_icon_btn()
    pp.display_cart_items()

    print('***** ADD TO CART SUCCESS ********')
    pp.checkout()

    assert CONFIRMATION_TEXT == pp.get_confirmation_text()
    print('***** CHECKOUT SUCCESS *****')

    pp.main_menu()
