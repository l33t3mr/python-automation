from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from Modules.custom_waits import wait_for_text_to_appear
from .BaseClass import BaseClass

import time


class DjangoAdmin(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        django_admin_interface = ''.join([self.driver.current_url[0:18], 'admin'])
        self.driver.get(django_admin_interface)

    def logout(self):
        logout = self.driver.find_element(By.CSS_SELECTOR, '#user-tools > a[href="/admin/logout/"]')
        logout.click()

    def create_superuser(self, username, password):
        # click on add users
        add_users = self.driver.find_element(By.CSS_SELECTOR, '.model-user > td:nth-child(2) > a:nth-child(1)')
        add_users.click()
        # fill in username and password
        username_field = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
        username_field.clear()
        username_field.send_keys(username)
        password_field = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
        password_field.clear()
        password_field.send_keys(password)
        password_field_confirmation = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')
        password_field_confirmation.clear()
        password_field_confirmation.send_keys(password)
        # save and continue editing button
        save_continue_btn = self.driver.find_element(By.CSS_SELECTOR, 'input[name="_continue"]')
        save_continue_btn.click()
        # give staff statu
        staff_status = self.driver.find_element(By.CSS_SELECTOR, '#id_is_staff')
        staff_status.click()
        # give superuser status
        superuser_status = self.driver.find_element(By.CSS_SELECTOR, '#id_is_superuser')
        superuser_status.click()
        # save and stop
        save_btn = self.driver.find_element(By.CSS_SELECTOR, 'input[name="_save"]')
        save_btn.click()

    def switch_to_view_site(self):
        view_site = self.driver.find_element(By.CSS_SELECTOR, '#user-tools > a:nth-child(2)')
        view_site.click()

    def delete_user(self, username):
        self.open()
        self._open_edit_users()
        self._search_for_user(username)
        # this includes deleting the user too
        self._delete_user_access_logs_and_account(username)

    def unblock_user(self, username):
        self.open()
        # self._open_acess_logs()
        # use search to narrow displayed table rows
        self._search_for_user(username)
        # this contains the delete function too
        self._delete_user_access_logs_and_account(username)

    def unblock_all_users(self):
        self.open()
        # self._open_acess_logs()
        # try:
        #     select_all_attempts = self.driver.find_element(By.CSS_SELECTOR, '#action-toggle')
        #     select_all_attempts.click()
        #     self.delete_all_users_access_logs()
        # except Exception:
        #     pass

    def _search_for_user(self, username):
        search = self.driver.find_element(By.CSS_SELECTOR, '#searchbar')
        search.clear()
        search.send_keys(username, Keys.ENTER)
        time.sleep(1)

    def _open_edit_users(self):
        edit_users = self.driver.find_element(By.CSS_SELECTOR, '.model-user > td:nth-child(3) > a:nth-child(1)')
        edit_users.click()

    def _open_acess_logs(self):
        edit_access_attempts = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/admin/axes/accessattempt/"]')
        edit_access_attempts.click()

    def _delete_user_access_logs_and_account(self, username):
        table_rows = self.driver.find_elements(By.CSS_SELECTOR, '#result_list > tbody > tr')
        for row in table_rows:
            username_field = row.find_element(By.CSS_SELECTOR, '.field-username')
            if username_field.text == username:
                checkbox = row.find_element(By.CSS_SELECTOR, '.action-checkbox > input.action-select')
                checkbox.click()
                self.delete_all_users_access_logs()
                return

    def delete_all_users_access_logs(self):
        action_dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, 'select[name="action"]'))
        action_dropdown.select_by_value('delete_selected')
        # click on go to execute selected option
        run_selected = self.driver.find_element(By.CSS_SELECTOR, '.button')
        run_selected.click()
        # confirm delete on the new page
        wait_for_text_to_appear(self.driver, 5, '#content > h1:nth-child(1)', 'Are you sure?')
        confirm_delete = self.driver.find_element(By.CSS_SELECTOR, 'input[value="Yes, I\'m sure"]')
        confirm_delete.click()

    def delete_all_users_except_list(self, users_to_not_delete_list=['admin', 'user']):
        self.open()
        self._open_edit_users()
        usernames = self.driver.find_elements(By.CSS_SELECTOR, '#result_list > tbody > tr > th.field-username')
        list_of_usernames = [x.text for x in usernames]
        # remove users that should not be deleted from extracted users
        [list_of_usernames.remove(x) for x in users_to_not_delete_list if x in list_of_usernames]
        for user in list_of_usernames:
            self._search_for_user(user)
            self._delete_user_access_logs_and_account(user)
        self.open()
        # self._open_acess_logs()
        # for user in list_of_usernames:
        #     self._search_for_user(user)
        #     self._delete_user_access_logs_and_account(user)
