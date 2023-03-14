from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .BaseClass import BaseClass

from Modules.custom_waits import wait_for_text_to_appear, wait_for_element_to_be_clickable


class MyProfile(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        my_profile = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/my_profile/"]')
        my_profile.click()

    def modify_my_profile(self, username, email=None, firstname=None, lastname=None,
                          timezone=None):
        self.enter_user_name(username)
        self.enter_email_address(email)
        self.enter_first_name(firstname)
        self.enter_last_name(lastname)
        self.select_time_zone(timezone)
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def get_my_profile_data(self):
        user_name = self._get_user_name()
        email_address = self._get_email_address()
        first_name = self._get_first_name()
        last_name = self._get_last_name()
        groups_list = self._get_groups()
        time_zone = self._get_time_zone()
        return {'username': user_name, 'email': email_address, 'firstname': first_name, 'lastname': last_name,
                'groups': groups_list, 'timezone': time_zone}

    def change_password(self, new_password):
        password_form = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/my_password/"]')
        password_form.click()
        wait_for_text_to_appear(self.driver, 10, '#main > h1:nth-child(2)', 'Change My Password')
        password_field = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
        password_field.send_keys(new_password)
        repeat_password_field = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')
        repeat_password_field.send_keys(new_password)
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def verify_change_password_message(self, text):
        message = self.driver.find_element(By.CSS_SELECTOR, '.row .alert.alert-danger')
        assert message.text == text, (
            'Failed to verify password change message. Current message{}'.format(message.text)
            , 'Expected Message {}'.format(text))

    def verify_group_not_editable(self):
        group = self.driver.find_element(By.CSS_SELECTOR, '.select2-search__field')
        assert not group.is_enabled(), 'Groupd can be edited!'

    def verify_message(self, text):
        message = self.driver.find_element(By.CSS_SELECTOR, '.alert.alert-success')
        assert message.text == text, ('Failed to verify message. Current message {}'.format(message.text),
                                      'Expected Message {}'.format(text))

    def wait_profile_loads(self):
        wait_for_element_to_be_clickable(self.driver, 10, '.btn.btn-primary')

    def enter_user_name(self, username):
        if username:
            username_input = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
            username_input.clear()
            username_input.send_keys(username)

    def enter_email_address(self, email):
        if email:
            email_input = self.driver.find_element(By.CSS_SELECTOR, '#id_email')
            email_input.clear()
            email_input.send_keys(email)

    def enter_first_name(self, first_name):
        if first_name:
            first_name_input = self.driver.find_element(By.CSS_SELECTOR, '#id_first_name')
            first_name_input.clear()
            first_name_input.send_keys(first_name)

    def enter_last_name(self, last_name):
        if last_name:
            last_name_input = self.driver.find_element(By.CSS_SELECTOR, '#id_last_name')
            last_name_input.clear()
            last_name_input.send_keys(last_name)

    def select_time_zone(self, timezone):
        if timezone:
            time_zone = Select(self.driver.find_element(By.CSS_SELECTOR, '#id_timezone'))
            time_zone.select_by_value(timezone)

    def _get_user_name(self):
        user_name = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
        return user_name.get_property('value')

    def _get_email_address(self):
        email_address = self.driver.find_element(By.CSS_SELECTOR, '#id_email')
        return email_address.get_property('value')

    def _get_first_name(self):
        first_name = self.driver.find_element(By.CSS_SELECTOR, '#id_first_name')
        return first_name.get_property('value')

    def _get_last_name(self):
        last_name = self.driver.find_element(By.CSS_SELECTOR, '#id_last_name')
        return last_name.get_property('value')

    def _get_groups(self):
        groups = self.driver.find_elements(By.CSS_SELECTOR, '.select2-selection__choice')
        groups_list = []
        [groups_list.append(group.get_property('title')) for group in groups]
        return groups_list

    def _get_time_zone(self):
        time_zone = Select(self.driver.find_element(By.CSS_SELECTOR, '#id_timezone'))
        return time_zone.first_selected_option.text
