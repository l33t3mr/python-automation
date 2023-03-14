import time
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
Definitions of states:

$$$ Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

clickable element : element is enabled (found in HTML DOM) and displayed/visible to user
visible element   : element is enabled (found in HTML DOM) and displayed/visible to user
invisible element : element either not enabled (not found in HTML DOM) or not displayed/visible to user
enabled element   : element is enabled (found in HTML DOM), not necessarily displayed/visible to user
disabled element  : element is disabled (not found in HTML DOM), definitely not displayed/visible to user
"""


def wait_for_element_to_be_clickable(driver, timeout, css_selector):
    try:
        time.sleep(2)
        wait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    except Exception:
        raise TimeoutError(
            'Waiting for Element with CSS Selector: {} timed out after {} seconds'.format(css_selector, timeout))


def wait_for_text_to_appear(driver, timeout, css_selector, text):
    try:
        time.sleep(2)
        wait(driver, timeout).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_selector), text))
    except Exception:
        raise TimeoutError(
            'Waiting for Element with CSS Selector: {} timed out after {} seconds'.format(css_selector, timeout))


def wait_for_element_to_be_invisible(driver, timeout, css_selector):
    try:
        return wait(driver, timeout).until(EC.invisibility_of_element((By.CSS_SELECTOR, css_selector)))
    except Exception:
        raise TimeoutError(
            'Waiting for Element with CSS Selector: {} timed out after {} seconds'.format(css_selector, timeout))


def wait_for_element_to_be_visible(driver, timeout, css_selector):
    try:
        wait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    except Exception:
        raise TimeoutError(
            'Waiting for Element with CSS Selector: {} timed out after {} seconds'.format(css_selector, timeout))


def wait_no_matching_records_appear_and_verify(driver, timeout, table_row_css_selector):
    wait_for_element_to_be_invisible(driver, timeout, 'div.fixed-table-container .fixed-table-loading')
    time.sleep(2)
    stop_time = time.time() + timeout
    while True:
        try:
            row = driver.find_element(By.CSS_SELECTOR, table_row_css_selector).text
            if row.lower() == 'no matching records found':
                return
        except AssertionError:
            raise AssertionError('Table row with text "No matching records found" could not be found. Current '
                               'table row text is {}'.format(row))
        finally:
            current_time = time.time()
            if current_time > stop_time:
                raise TimeoutError('Table row with text "No matching records found" could not be found. Current '
                                   'table row text is {}'.format(row))
