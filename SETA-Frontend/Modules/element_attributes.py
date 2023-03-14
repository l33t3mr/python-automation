from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def element_visible_and_enabled(driver, css_selector):
    '''
    To check that an element is clickable, it has to be enabled and displayed
    :param driver: selenium webdriver
    :param css_selector:  css selector
    '''
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        if element.is_displayed() and element.is_enabled():
            return True
    except NoSuchElementException:
        return False


def element_exists_within_object(web_object, element_css_selector):
    try:
        web_object.find_element(By.CSS_SELECTOR, element_css_selector)
        return True
    except NoSuchElementException:
        return False


def element_exists_by_link_text(driver, link_text):
    try:
        driver.find_element(By.LINK_TEXT, link_text)
        return True
    except NoSuchElementException:
        return False


def element_is_visible(driver, css_selector):
    return driver.find_element(By.CSS_SELECTOR, css_selector).is_displayed()
