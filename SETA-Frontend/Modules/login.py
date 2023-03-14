from selenium.webdriver.common.by import By

from Modules.authorization_info import login_url
from Modules.custom_waits import wait_for_element_to_be_clickable


def login(driver, in_user, in_password):
    # Entering Username
    if 'accounts/login/' not in driver.current_url:
        driver.get(login_url)
        wait_for_element_to_be_clickable(driver, 5, '.btn.btn-primary')
    username = driver.find_element(By.CSS_SELECTOR, '#login-username')
    username.send_keys(in_user)
    # Entering password
    password = driver.find_element(By.CSS_SELECTOR, '#login-password')
    password.send_keys(in_password)
    # verify Login button can be seen and clicked
    find_login_btn = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
    find_login_btn.click()


def verify_failed_login(driver):
    failed_message = driver.find_element(By.CSS_SELECTOR, '.col-sm-6 > p')
    assert failed_message.text == 'Your username and password didn\'t match. Please try again.', (
        'Failed Login Message mismatches. Current failed login Message is {}'.format(failed_message.text))


def verify_successfull_login(driver):
    reports_view_heading = driver.find_element(By.CSS_SELECTOR, 'h1')
    assert reports_view_heading.text == 'Reports', (
        'Login Failed Reports in Navbar cannot be found. Current Text is {}'.format(reports_view_heading.text))


def verify_account_blocked(driver):
    block_message = driver.find_element(By.CSS_SELECTOR, '.lead')
    block_heading = driver.find_element(By.CSS_SELECTOR, 'h1')
    assert block_message.text == 'Account has been locked: too many login attempts. Please try again later.', (
        'Blocked Account Message mismatches. Current blocked account Message is {}'.format(block_message.text))
    assert block_heading.text == 'An error has occurred', ('Blocked Account Header text mismatches.'
                                                           ' Current Header text is{}'.format(block_heading.text))


def verify_login_page_open(driver):
    assert '/accounts/login' in driver.current_url
