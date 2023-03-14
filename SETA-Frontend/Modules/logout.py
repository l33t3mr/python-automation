from selenium.webdriver.common.by import By

from Modules.element_attributes import element_visible_and_enabled
from Modules.custom_waits import wait_for_element_to_be_visible


def logout(driver):
    logout_btn = driver.find_element(By.CSS_SELECTOR, '.logout-button > span')
    logout_btn.click()
    wait_for_element_to_be_visible(driver, 5, '.main-heading-container > h2#content')
    logout_text = driver.find_element(By.CSS_SELECTOR, '.main-heading-container > h2#content')
    assert logout_text.text == 'Logged out!', (
        '"{}" not found, text found is: {}'.format('Logged out!', logout_text.text))


def logout_clickable(driver):
    return element_visible_and_enabled(driver, '.fa-sign-out')
