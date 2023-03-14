from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from .MyProfile import MyProfile
from Modules.element_attributes import element_visible_and_enabled
from Modules.custom_waits import wait_for_element_to_be_clickable, wait_no_matching_records_appear_and_verify, \
    wait_for_text_to_appear


class Users(MyProfile):

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        users = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/users/"]')
        users.click()

    def verify_user_cannot_see_users_tab(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        assert not element_visible_and_enabled(self.driver, 'a[href="/settings/users/"]'), 'Users Tab is visible'

    def create_new_user(self, username, email=None, first_name=None, last_name=None, group=None, password=None,
                        view_permissions=None, timezone=None, csv_header='check', csv_delimiter=',',
                        create_non_anonymized=None):
        """
        Creates a new user.

        :param username: str
        :param email: str
        :param first_name: str
        :param last_name: str
        :param group: str
        :param password: str
        :param view_permissions: list(str) of needed view_permissions. must match the name of the view permissions
        in the create user form.
        :param timezone: str must match the name of the timezone in the create user form
        :param csv_header: bool to put a check-mark True, remove with False
        :param csv_delimiter: bool to put a check-mark True, remove with False
        :param create_non_anonymized:bool to put a check-mark True, remove with False
        """
        create_user_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        create_user_btn.click()
        self.enter_user_name(username)
        self.enter_email_address(email)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self._enter_repeat_password(password)
        self._enter_group(group)
        self._enter_viewing_permissions(view_permissions)
        self.select_time_zone(timezone)
        self._check_uncheck_csv_header(csv_header)
        self._select_csv_delimiter(csv_delimiter)
        self._create_non_anonymized_report(create_non_anonymized)
        create_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        create_button.click()

    def modify_existing_user(self, username, email=None, first_name=None, last_name=None, group=None,
                             view_permissions=None, timezone='Europe/Berlin', csv_header=None, csv_delimiter=',',
                             create_non_anonymized=None):

        """
        Modifies an existing user by replacing current values in user-form with the parameter values passed into it.

        :param username: str automatically clears field, before writing new value to it
        :param email: str automatically clears field, before writing new value to it
        :param first_name: str automatically clears field, before writing new value to it
        :param last_name: str automatically clears field, before writing new value to it
        :param group: str clears all groups if passed 'clear' otherwise adds to existing groups
        :param view_permissions: list(str) automatically clears all permissions and adds permissions from the list.
         Permissions must match the name of the view permissions in the create user form.
        :param timezone: str must match the name of the timezone in the create user form
        :param csv_header: bool to put a check-mark True, remove with False
        :param csv_delimiter: bool to put a check-mark True, remove with False
        :param create_non_anonymized:bool to put a check-mark True, remove with False
        """

        self.enter_user_name(username)
        self.enter_email_address(email)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self._enter_group(group)
        self._enter_viewing_permissions_modify_user(view_permissions)
        self.select_time_zone(timezone)
        self._check_uncheck_csv_header(csv_header)
        self._select_csv_delimiter(csv_delimiter)
        self._create_non_anonymized_report(create_non_anonymized)
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def change_password(self, new_password):
        password_form = self.driver.find_element(By.CSS_SELECTOR, '.col-md-9 a')
        password_form.click()
        password_field = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
        password_field.send_keys(new_password)
        repeat_password_field = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')
        repeat_password_field.send_keys(new_password)
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def find_and_modify_user_via_edit_operation(self, username):
        find_user = self._search_user(username)
        edit_operation = find_user.find_element(By.CSS_SELECTOR, '.fa.fa-edit')
        edit_operation.click()

    def find_and_delete_user_via_delete_operation(self, username):
        find_user = self._search_user(username)
        delete_operation = find_user.find_element(By.CSS_SELECTOR, '.fa.fa-trash')
        delete_operation.click()

    def confirm_user_delete(self):
        self._wait_confirmation_window_appears()
        button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-danger')
        button.click()

    def verify_content_of_delete_confirmation_page(self, username):
        self._wait_confirmation_window_appears()
        question = self.driver.find_element(By.CSS_SELECTOR, '#main > form:nth-child(3) > p:nth-child(2)')
        h1 = self.driver.find_element(By.CSS_SELECTOR, '#main > h1')
        username_from_page = self.driver.find_element(By.CSS_SELECTOR, '#main ul > li')
        note = self.driver.find_element(By.CSS_SELECTOR, '#main > form:nth-child(3) > p:nth-child(4)')
        confirm_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-danger')
        back_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-secondary')
        assert h1.text == 'Delete User', 'H1 in page does not have "Delete User"'
        assert username_from_page.text == username, 'Username on page does not match given argument {}'.format(username)
        assert question.text == 'Are you sure you want to delete the following users?', (
            'Question to confirm delete mismatch')
        assert note.text == 'Note : All reports owned by a user will be deleted as well!', 'Note text mismatch'
        assert confirm_btn.get_property('value') == 'Confirm', 'Confirm button label mismatch'
        assert back_btn.text == 'Back', 'Back button label mismatch'

    def verify_user_deleted(self, username):
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#main .form-control')
        search_box.send_keys(username, Keys.TAB)
        wait_no_matching_records_appear_and_verify(self.driver, 10, '#user-list > tbody > tr > td')
        search_box.clear()

    def _verify_error_message(self, css_selector, error_text):
        message = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        assert message.text == error_text, 'Error message mismatched. Expected error message {}'.format(error_text)

    def verify_message(self, text):
        self._verify_error_message('.alert.alert-success', text)

    def verify_change_password_message(self, text):
        self._verify_error_message('.row .alert.alert-danger', text)

    def wait_mapping_load(self):
        wait_for_element_to_be_clickable(self.driver, 5, '.fa.fa-edit')

    def verify_user_cannot_edit_other_users_profiles(self, username):

        """
        Verifies that the currently logged in user, cannot edit the user profile passed as argument.
        It verifies that the "Edit" under operations is greyed out and disabled/not clickable.

        :param username: str
        """

        user_row = self._search_user(username)
        user_row_select_checkbox = user_row.find_element(By.CSS_SELECTOR, 'input')
        assert not user_row_select_checkbox.is_enabled(), 'User {} selection checkbox is enabled!'.format(username)
        user_row_edit = user_row.find_element(By.CSS_SELECTOR, '.fa.fa-edit')
        assert user_row_edit.get_attribute('class') == 'fa fa-edit disabled', (
            'User {} Edit Icon is Enabled!'.format(username))

    def verify_user_cannot_delete_other_users_profiles(self, username):
        user_row = self._search_user(username)
        user_row_select_checkbox = user_row.find_element(By.CSS_SELECTOR, 'input')
        assert not user_row_select_checkbox.is_enabled(), 'User {} selection checkbox is enabled!'.format(username)
        user_removal_control = user_row.find_element(By.CSS_SELECTOR, '.fa.fa-trash').get_attribute('class')
        assert user_removal_control == 'fa fa-trash disabled', 'User {} Trash Icon is Enabled!'.format(username)

    def remove_group_in_user_form(self, group_name):
        groups = self.driver.find_elements(By.CSS_SELECTOR, '.select2-selection__rendered li')
        for group in groups:
            if group.get_attribute('title') == group_name:
                group.find_element(By.CSS_SELECTOR, '.select2-selection__choice__remove').click()
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def clear_groups_field_in_user_form(self):
        user_groups_field = self.driver.find_elements(
            By.CSS_SELECTOR, 'li.select2-selection__choice')
        user_groups_count = len(user_groups_field)
        for group in range(user_groups_count):
            self.driver.find_element(By.CSS_SELECTOR, '.select2-selection__choice__remove').click()
        update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update_button.click()

    def delete_all_users_except_list_and_superuser(self, users_to_not_delete_list=['admin'], superuser='user'):
        users_to_not_delete_list.append(superuser)
        while True:
            users_table = self.driver.find_elements(By.CSS_SELECTOR, '#user-list > tbody > tr > td')
            # count how many rows are in table, if count = nr. of users not to be deleted break
            if len(users_table) / 8 == len(users_to_not_delete_list):
                return
            users_table_data = [data.text for data in users_table]
            users_list_to_delete = []
            # a row has 8 (index:0-8) elements, first username has index '1', add '8', get the next user in next row
            for index in range(1, len(users_table_data), 8):
                users_list_to_delete.append(users_table_data[index])
            for user in users_list_to_delete:
                if user not in users_to_not_delete_list:
                    self.find_and_delete_user_via_delete_operation(user)
                    self.confirm_user_delete()

    def _enter_group(self, group):
        if group == 'clear':
            self.clear_groups_field_in_user_form()
        elif group:
            group_name = self.driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(6) > div.col-md-9'
                                                                   ' > span.select2-container span.select2-selection'
                                                                   ' > ul > li.select2-search > input')
            group_name.send_keys(group, Keys.ENTER)
            group_name.send_keys(Keys.TAB)

    def _enter_viewing_permissions(self, view_permissions):
        if view_permissions:
            for permission in view_permissions:
                permissions_field = self.driver.find_element(By.CSS_SELECTOR,
                                                             'div.form-group:nth-child(9) > div.col-md-9'
                                                             ' > span.select2-container '
                                                             'span.select2-selection > ul'
                                                             ' > li.select2-search > input')
                permissions_field.send_keys(permission, Keys.ENTER)
                permissions_field.send_keys(Keys.TAB)

    def _clear_viewing_permissions_field(self):
        permissions_removal_control = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group:nth-child(8)'
                                                                                 ' > div:nth-child(2)'
                                                                                 ' > span:nth-child(2)'
                                                                                 ' > span:nth-child(1)'
                                                                                 ' > span:nth-child(1)'
                                                                                 ' > ul:nth-child(1) > li > '
                                                                                 '.select2-selection__choice__remove')
        for count in range(len(permissions_removal_control)):
            remove_permission = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group:nth-child(8)'
                                                                           ' > div:nth-child(2) > span:nth-child(2)'
                                                                           ' > span:nth-child(1) > span:nth-child(1)'
                                                                           ' > ul:nth-child(1) > li'
                                                                           ' > .select2-selection__choice__remove')
            remove_permission.click()

    def _enter_viewing_permissions_modify_user(self, view_permissions):
        if view_permissions:
            self._clear_viewing_permissions_field()
            permissions_field = self.driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(8) > div.col-md-9'
                                                                          ' > span.select2-container'
                                                                          ' span.select2-selection > ul'
                                                                          ' > li.select2-search > input')
            for permission in view_permissions:
                permissions_field.send_keys(permission, Keys.ENTER)
            permissions_field.send_keys(Keys.TAB)

    def _enter_repeat_password(self, passwd):
        if passwd:
            password = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
            password.send_keys(passwd)
            repeat_password = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')
            repeat_password.send_keys(passwd)

    def _check_uncheck_csv_header(self, csv_header):
        if csv_header:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, '#id_csv_header')
            if checkbox.is_selected() and not csv_header:
                checkbox.click()
                assert not checkbox.is_selected(), 'Failed to disable CSV checkbox'
            elif not checkbox.is_selected() and csv_header:
                checkbox.click()
                assert checkbox.is_selected(), 'Failed to enable CSV checkbox'

    def _select_csv_delimiter(self, delimiter):
        if delimiter:
            select = Select(self.driver.find_element(By.CSS_SELECTOR, '#id_csv_delimiter'))
            select.select_by_value(delimiter)

    def _create_non_anonymized_report(self, create_non_anonymized):
        if create_non_anonymized:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, '#id_create_non_anonymized_reports')
            if create_non_anonymized and not checkbox.is_selected():
                checkbox.click()
                assert checkbox.is_selected(), 'Failed to enable "Create non anonymized reports'
            elif not create_non_anonymized and checkbox.is_selected():
                checkbox.click()
                assert not checkbox.is_selected(), 'Failed to disabled "Create non anonymized reports'

    def _search_user(self, username):
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'input.form-control')
        search_box.clear()
        self.wait_mapping_load()
        search_box.send_keys(username)
        self.wait_mapping_load()
        user_table = self.driver.find_elements(By.CSS_SELECTOR, '#user-list > tbody > tr')
        for row in user_table:
            data = row.find_elements(By.CSS_SELECTOR, 'td')
            if data[1].text == username:
                return row
        raise AssertionError('User {} not found'.format(username))

    def _wait_confirmation_window_appears(self):
        wait_for_text_to_appear(self.driver, 10, '#main > form:nth-child(3) > p:nth-child(2)',
                                'Are you sure you want to delete the following users?')

    def _buffer_groups_names(self):
        groups = self.driver.find_elements(By.CSS_SELECTOR, '.select2-selection__rendered > li')
        groups_names_list = [e.get_attribute('title') for e in groups if e.text]
        return groups_names_list
