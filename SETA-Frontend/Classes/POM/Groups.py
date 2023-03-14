from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from .BaseClass import BaseClass

from Modules.custom_waits import wait_for_element_to_be_clickable, wait_for_element_to_be_invisible


class Groups(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        groups = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/groups/"]')
        groups.click()

    def groups_tab_invisible(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        assert wait_for_element_to_be_invisible(self.driver, 5, 'a[href="/settings/groups/"]')

    def create_group(self, groupname, users_list=None, view_permissions=None, create_non_anonymized=None):
        self._create_group_button()
        self._enter_group_name(groupname)
        self._add_users(users_list)
        self._add_view_permissions(view_permissions)
        self._anonymize_report(create_non_anonymized)
        form_create_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        form_create_button.click()

    def modify_group(self, groupname, users_list=None, view_permissions=None, create_non_anonymized=None):
        # automatically clear all usernames in users field
        group_name = self.driver.find_element(By.CSS_SELECTOR, '#id_name')
        group_name.clear()
        group_name.send_keys(groupname, Keys.TAB)
        self._clear_users_field()
        self._clear_view_permissions_field()
        self._add_users(users_list)
        self._add_view_permissions(view_permissions)
        self._anonymize_report(create_non_anonymized)
        form_update_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        form_update_button.click()

    def find_group_modify_via_operations(self, groupname):
        find_group = self._search_group(groupname)

        edit_operation = find_group.find_element(By.CSS_SELECTOR, '.fa.fa-edit')
        edit_operation.click()

    def find_group_delete_via_operations(self, groupname):
        find_group = self._search_group(groupname)
        delete_operation = find_group.find_element(By.CSS_SELECTOR, '#group-list > tbody .fa.fa-trash')
        delete_operation.click()

    def verify_message(self, text):
        message = self.driver.find_element(By.CSS_SELECTOR, '.alert.alert-success')
        assert message.text == text

    def confirm_group_delete(self):
        button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-danger')
        button.click()

    def verify_delete_confirmation_content(self, groupname):
        question = self.driver.find_element(By.CSS_SELECTOR, '#main > form:nth-child(3) > p:nth-child(2)')
        h1 = self.driver.find_element(By.CSS_SELECTOR, '#main > h1')
        group_name = self.driver.find_element(By.CSS_SELECTOR, '#main ul > li')
        assert h1.text == 'Delete Group'
        assert group_name.text == groupname
        assert question.text == 'Are you sure you want to delete the following groups?'

    def verify_group_deleted(self, groupname):
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#main .form-control')
        search_box.send_keys(groupname, Keys.TAB)
        wait(self.driver, 10).until(
            ec.text_to_be_present_in_element((By.CSS_SELECTOR, '#group-list > tbody > tr > td'),
                                             'No matching records found'))
        search_box.clear()

    def verify_can_not_delete_admin_group(self):
        admin_group_row = self._search_group('admin')
        admin_group_select_checkbox = admin_group_row.find_element(By.CSS_SELECTOR, 'input')
        if admin_group_select_checkbox.is_enabled() is True:
            raise AssertionError('Admin Group Selection Checbox is Enabled!')

    def verify_group_name_disabled_and_hint(self):
        group_name = self.driver.find_element(By.CSS_SELECTOR, '#id_name')
        assert group_name.is_enabled() is False
        group_hint = self.driver.find_element(By.CSS_SELECTOR, 'small.form-text:nth-child(2)')
        assert group_hint.text == 'The name of the "admin" group cannot be changed.'
        non_anonymized_checkbox = self.driver.find_element(By.CSS_SELECTOR, '#id_create_non_anonymized_reports')
        assert non_anonymized_checkbox.is_enabled() is False
        users_hint = self.driver.find_element(By.CSS_SELECTOR, '.form-check > small:nth-child(3)')
        assert users_hint.text == 'This option cannot be disabled for group "admin".'

    def wait_mapping_load(self):
        wait_for_element_to_be_clickable(self.driver, 5, '.fa.fa-edit')

    # TODO: refactor to use select all in groups as it automatically deselects admin group
    def delete_all_groups_except_list(self, groups_to_not_delete_list=['admin']):
        while True:
            groups_table = self.driver.find_elements(By.CSS_SELECTOR, '#group-list > tbody > tr > td')
            # count how many rows are in table, if count = nr. of groups not to be deleted break
            if len(groups_table) / 4 == len(groups_to_not_delete_list):
                return
            groups_table_data = [data.text for data in groups_table]
            groups_list_to_delete = []
            # a row has 4 (index:0-3) elements, first username has index '1', add '4', get the next user in next row
            for index in range(1, len(groups_table_data), 4):
                groups_list_to_delete.append(groups_table_data[index])
            for group in groups_list_to_delete:
                if group not in groups_to_not_delete_list:
                    self.find_group_delete_via_operations(group)
                    self.confirm_group_delete()

    def _anonymize_report(self, create_non_anonymized):
        if create_non_anonymized is not None:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, '#id_create_non_anonymized_reports')
            if create_non_anonymized is True and checkbox.is_selected() is False:
                checkbox.click()
            elif create_non_anonymized is False and checkbox.is_selected() is True:
                checkbox.click()

    def _search_group(self, groupname):
        group_search_input = self.driver.find_element(By.CSS_SELECTOR, 'input.form-control')
        group_search_input.clear()
        self.wait_mapping_load()
        group_search_input.send_keys(groupname)
        self.wait_mapping_load()
        group_table_rows = self.driver.find_elements(By.CSS_SELECTOR, '#group-list > tbody > tr')
        for row in group_table_rows:
            table_row_td = row.find_elements(By.CSS_SELECTOR, 'td')
            if table_row_td[1].text == groupname:
                return row
        raise AssertionError('Group not found')

    def _create_group_button(self):
        groups_create_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        groups_create_button.click()

    def _clear_users_field(self):
        users_field = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group.row:nth-child(3)'
                                                                 ' .select2.select2-container ul'
                                                                 ' > li.select2-selection__choice')
        for count in range(len(users_field)):
            delete_saved_users = self.driver.find_element(By.CSS_SELECTOR,
                                                          'div.form-group.row:nth-child(3) .select2-search__field')
            delete_saved_users.send_keys(Keys.BACK_SPACE)
            delete_saved_users.send_keys(Keys.TAB)

    def _clear_view_permissions_field(self):
        permissions_field = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group.row:nth-child(4)'
                                                                       ' .select2.select2-container ul'
                                                                       ' > li.select2-selection__choice')
        for count in range(len(permissions_field)):
            delete_saved_permissions = self.driver.find_element(By.CSS_SELECTOR, 'div.form-group.row:nth-child(4)'
                                                                                 ' .select2-search__field')
            delete_saved_permissions.send_keys(Keys.BACK_SPACE)
            delete_saved_permissions.send_keys(Keys.TAB)

    def _enter_group_name(self, groupname):
        group_name = self.driver.find_element(By.CSS_SELECTOR, '#id_name')
        group_name.send_keys(groupname)

    def _add_users(self, users_list):
        if users_list is not None:
            for user in users_list:
                user_field = self.driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(3) > div.col-md-9'
                                                                       ' > span.select2-container'
                                                                       ' span.select2-selection > ul'
                                                                       ' > li.select2-search > input')
                user_field.send_keys(user, Keys.ENTER)
                user_field.send_keys(Keys.TAB)

    def _add_view_permissions(self, view_permissions):
        if view_permissions is not None:
            for permission in view_permissions:
                permission_field = self.driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(4)'
                                                                             ' > div.col-md-9 > span.select2-container'
                                                                             ' span.select2-selection > ul'
                                                                             ' > li.select2-search > input')
                permission_field.send_keys(permission, Keys.ENTER)
                permission_field.send_keys(Keys.TAB)

    def _wait_delete_button_clickable(self):
        wait(self.driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-danger')))
