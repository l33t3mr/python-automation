from abc import ABC
from selenium.webdriver.common.by import By

class BaseClass(ABC):
    def __init__(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def get_logged_in_user(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.navbar-link').text

    def is_user_logged_in(self, username):
        return self.driver.find_element(By.CSS_SELECTOR, '.navbar-link').text == username

    def set_driver(self, driver):
        self.driver = driver
