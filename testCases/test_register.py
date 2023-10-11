import pytest
from selenium.webdriver.support.select import Select
from pageElements.register import Register
from pageElements.login import Login
from testData.register_data import register_scenario
from utils.variables import DUPLICATE_USER, REGISTER_URI, DEFAULT_CATEGORY, DEFAULT_LANG


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
