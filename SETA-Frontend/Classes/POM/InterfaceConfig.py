import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from .BaseClass import BaseClass

from Modules.element_attributes import element_visible_and_enabled
from Modules.custom_waits import wait_no_matching_records_appear_and_verify, wait_for_element_to_be_invisible, \
    wait_for_element_to_be_clickable, wait_for_element_to_be_visible
from Data.data_path import DOWNLOAD_DIR_PATH


class InterfaceConfig(BaseClass):

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        self._wait_interface_config_label_loads()
        ic_configs = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/interface_config/"]')
        ic_configs.click()

    def get_status(self):
        """
        This function reads the upload status in Interface/Ip Mapping.
        The status consists of three part as in this example:
        - Successfull Status -> Green box, OK, Latest Active version since: YYYY-MM-DD HH:MM:s
        - Failed Status      -> Red box, Failed, Latest Active version since: YYYY-MM-DD HH:MM:s, some error message

        :return: (dict) with keys "status_color", "status_label","active_version"
        """

        color = self.driver.find_element(By.ID, 'status-progress').value_of_css_property('background-color')
        color_dict = {'rgb(220, 53, 69)': 'RED', 'rgb(40, 167, 69)': 'GREEN', 'rgb(0, 123, 255)': 'BLUE'}
        status_color = color_dict[color]
        status_label = self.driver.find_element(By.ID, 'status-label').text
        active_version = self.driver.find_element(By.ID, 'createdAt').text
        return {'status color': status_color, 'status label': status_label, 'active version': active_version}

    def upload_mapping(self, file_path, toggle_header=True,
                       delimiter=None, form_button='upload'):
        """
        This function uploads a mapping file by:
         1- opening 'Actions -> Upload Mapping' Window
         2- file_path : path to the file to be uploaded
         3- toggle_header: marks the checkbox with value True or unmark it with False
         4- delimiter: choose between ; and , as delimiters
         5-form_button: either upload or cancel as values"""

        self._open_actions_menu()
        self._select_download_or_upload('upload mappings')
        self._toggle_header(toggle_header)
        self._select_delimiter(delimiter)
        self._upload_file(file_path)
        self._confirm_or_cancel_upload(form_button)
        self.wait_upload_modal_disappears()

    def download_mapping(self):
        self._open_actions_menu()
        self._select_download_or_upload('download mappings')

    def is_add_entries_to_mapping_enabled(self):
        """
        Checks if the "+" element in the "Add Mapping" section can be found in the page HTML or not.
        :return: (bool)
        """
        return element_visible_and_enabled(self.driver, '#table-new-mapping > tbody > tr > td .fa.fa-plus')

    def is_upload_mappings_enabled(self):
        """
        Checks if the HTML link element <a> to upload the Mapping can be found in the page HTML or not.
        :return: (bool)
        """

        self._open_actions_menu()
        return element_visible_and_enabled(self.driver, 'a[data-target="#uploadMappingFile"]')

    def clear_failed_uploads_or_cancel_pending_uploads(self):
        """
        This is used to clear failed uploads or cancel pending uploads since both buttons, use the exact
        same CSS Selector
        """
        wait_for_element_to_be_clickable(self.driver, 5, '#status-btn-del-pending')
        button_element = self.driver.find_element(By.CSS_SELECTOR, '#status-btn-del-pending')
        button_element.click()
        wait_for_element_to_be_invisible(self.driver, 30, '#status-btn-del-pending')

    def wait_upload_modal_disappears(self):
        """
        Waits for the Upload Modal Dialog that appears after uploading a mapping file to disappear. 
        """
        wait_for_element_to_be_invisible(self.driver, 30, '#pleaseWaitDialog')

    def wait_for_add_entry_table_to_load(self):
        """ 
        Waits for add new entry section table to load
        """
        wait_for_element_to_be_clickable(self.driver, 5, '#table-new-mapping > tbody > tr > td .fa.fa-plus')

    def wait_status_color_stabilizes(self):
        """
        Waits for the Status Color to turn either RED or GREEN, then return.
        It waits for less than 600 seconds, before terminating and raising an TimeoutError.
        600 seconds is the limit since some Mapping could take up to 10 minutes to be processed.
        """
        status_color = self.driver.find_element(By.CSS_SELECTOR, '#status-progress')
        start_time = time.time()
        while status_color.value_of_css_property('background-color') not in ['rgb(40, 167, 69)', 'rgb(220, 53, 69)']:
            time.sleep(1)
            current_time = time.time()
            if current_time - start_time >= 600:
                raise TimeoutError(
                    'Exceeded wait time for Mapping Status Color to stabilize,current color in mapping is {}'.format(
                        status_color.value_of_css_property('background-color')))
        self.wait_for_add_entry_table_to_load()

    def add_entries(self, list_of_tuples):
        """
        Will add entries entered as a list of tuples(first_node, second_node,interface,direction)
        """
        self.wait_for_add_entry_table_to_load()
        rows_count = len(list_of_tuples)
        # N-entries need N-1 clicks to add row in 'Add New Entry to Mapping"
        for row in range(rows_count - 1):
            add_row_control = self.driver.find_element(By.CSS_SELECTOR,
                                                       '#table-new-mapping > tbody > tr > td .fa.fa-plus')
            add_row_control.click()
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-new-mapping > tbody > tr')
        for index in range(rows_count):
            first_node, second_node, interface = rows[index].find_elements(By.CSS_SELECTOR, 'input')
            first_node.send_keys(list_of_tuples[index][0])
            second_node.send_keys(list_of_tuples[index][1])
            interface.send_keys(list_of_tuples[index][2])
            # direction needs special handling: open it, then select proper value
            direction_dropdown = rows[index].find_element(By.CSS_SELECTOR, '.select2-selection__rendered')
            direction_dropdown.click()
            self._choose_direction(list_of_tuples[index][3])
        add_node_button = self.driver.find_element(By.CSS_SELECTOR, '#new-mapping-form > .btn.btn-primary')
        add_node_button.click()

    def verify_message_upload_csv(self, text):
        self._verify_message('#status-message.alert.alert-danger', text)

    def verify_message_file_must_be_csv(self):
        expected_text = 'File must be a CSV file'
        self._verify_message('#main > .alert.alert-danger', expected_text)

    def verify_message_add_entry(self, error_text):
        self._verify_message('#new-mapping-form-message .alert', error_text)

    def verify_message_delete(self, error_text):
        self._verify_message('#delete-error-message > .alert', error_text)

    def delete_entries(self, list_of_tuples):
        """
        Will delete entries by clicking on the "x" control corresponding to the entry in the Mapping.

        :param list_of_tuples: (list) of tuples each tuple in the following order:
        1- Interface Config Tuple (first_node, second_node,interface,direction)
        2- Ip Mapping Tuple (node_name, ims_entity, ip_address)
        """
        for entry in list_of_tuples:
            self._wait_mapping_table_load()
            search = self.driver.find_element(By.CSS_SELECTOR, '#mapping-container input[class="form-control"]')
            search.send_keys(entry[1], Keys.ENTER)
            self._wait_mapping_table_load()
            tbody_rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-ip-mappings > tbody > tr')
            for row in tbody_rows:
                # using assert
                if row.text == ' '.join(entry[0:3]):
                    remove_row_control = row.find_element(By.CSS_SELECTOR, '.fa.fa-remove')
                    remove_row_control.click()
                    break
            search.clear()

    def verify_deleted(self, list_of_tuples):
        """
        verify deleted entries can't be found in Config/Mapping Table anymore

        :param list_of_tuples: (list) of tuples each tuple in the following order:
        1- Interface Config Tuple (first_node, second_node,interface,direction)
        2- Ip Mapping Tuple (node_name, ims_entity, ip_address)
        """
        for entry in list_of_tuples:
            self._wait_mapping_table_load()
            search = self.driver.find_element(By.CSS_SELECTOR, '#mapping-container input[class="form-control"]')
            search.clear()
            search.send_keys(entry[2].lower(), Keys.ENTER)
            time.sleep(2)
            rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-ip-mappings > tbody > tr')
            rows_text = [x.text for x in rows]
            current_entry = ' '.join(entry[0:3])
            assert current_entry not in rows_text, 'Entry () was not deleted'.format(current_entry)
            search.clear()

    def bulk_delete(self, list_of_entries_tuples):
        """
        Will delete entries entered as a list of tuples(first_node, second_node,interface,direction) by selecting
        the matching entries in the Mapping and clicking the "Delete" button to delete them all in one go.

        :param list_of_entries_tuples: (list) of tuples each tuple in the following order:
        1- Interface Config Tuple (first_node, second_node,interface,direction)
        2- Ip Mapping Tuple (node_name, ims_entity, ip_address)
        """
        self._wait_mapping_table_load()
        tbody_rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-ip-mappings > tbody > tr')
        for row in tbody_rows:
            cells = row.find_elements(By.CSS_SELECTOR, 'td')
            cells_checkbox = row.find_element(By.CSS_SELECTOR, 'input')
            '''Cells would have the following text values:
            1- Interface Config: ['','first_node','','second_node','interface', '']
            2- Ip Mapping : ['', 'node_name','ims_entity','ip_address','']
            '''
            for entry in list_of_entries_tuples:
                if cells[1].text == entry[0] and cells[3].text == entry[1]:
                    cells_checkbox.click()
                    assert cells_checkbox.is_selected() is True
                    break
        delete_button = self.driver.find_element(By.CSS_SELECTOR, '#btn-delete-mappings')
        delete_button.send_keys(Keys.ENTER)
        self._wait_mapping_table_load()

    def delete_all_config(self):
        """
        Will select all entries in the table on the current open PAGE/TABLE PAGE and click "delete" button
        """
        self._wait_mapping_table_load()
        check_all = self.driver.find_element(By.CSS_SELECTOR, '#table-ip-mappings > thead > tr > th')
        check_all.click()
        delete_button = self.driver.find_element(By.CSS_SELECTOR, '#btn-delete-mappings')
        delete_button.send_keys(Keys.ENTER)
        self._wait_mapping_table_load()

    def get_help_verify(self):
        """
        Will verify the text that appears when user clicks on "?" next to the Interface Configuration Label on the left
        navibar
        """
        get_help = self.driver.find_element(By.CSS_SELECTOR,
                                            'a[href="/help_text/interface_config/"] .fa-question-circle')
        main_window_handle = self.driver.window_handles[0]
        get_help.click()
        all_windows_handles = self.driver.window_handles
        for handle in all_windows_handles:
            if handle != main_window_handle:
                self.driver.switch_to.window(handle)
                wait(self.driver, 10).until(ec.text_to_be_present_in_element(
                    (By.TAG_NAME, 'h1'), 'Interface Config'))
                header_csv_style = self.driver.find_element(By.TAG_NAME, 'h4')
                help_text = self.driver.find_element(By.TAG_NAME, 'p')
                mandatory = self.driver.find_element(By.TAG_NAME, 'ul')
                # assert header_ip_mapping.text == 'Interface Config'
                assert header_csv_style.text == ('Help: CSV style for uploading '
                                                 'interface configurations'), 'Header mismatches'
                assert help_text.text == ('The CSV must have the columns:\nfirst_node, second_node, direction,'
                                          ' interface\nThe columns must be in this order! You can specify if you have'
                                          ' a headline or not.\nYou can choose between following delimiters: , ;'
                                          '\nThe following is a list of rules for mandatory interfaces which should be '
                                          'included in interface configurations:'), 'Help Text mismatches'

                assert mandatory.text == "('UA', ?, 'both', 'Gm') OR (?, 'UA', 'both', 'Gm')"
                self.driver.close()
        self.driver.switch_to.window(main_window_handle)

    def _wait_no_matching_records_found_appear(self):
        wait_no_matching_records_appear_and_verify(self.driver, 5, '#table-ip-mappings > tbody > tr')

    def _open_actions_menu(self):
        dropdown_open_status = self.driver.find_element(By.CSS_SELECTOR, '.dropdown').get_attribute('class')
        if not dropdown_open_status == 'dropdown show':
            dropdown_menu = self.driver.find_element(By.CSS_SELECTOR, '#dropdownMenuButton')
            dropdown_menu.send_keys(Keys.ENTER)

    def _select_download_or_upload(self, action):
        if action == 'upload mappings':
            upload_mappings_from_dropdown = self.driver.find_element(By.CSS_SELECTOR,
                                                                     'a[data-target="#uploadMappingFile"]')
            wait_for_element_to_be_clickable(self.driver, 5, 'a[data-target="#uploadMappingFile"]')
            upload_mappings_from_dropdown.click()
        elif action == 'download mappings':
            download_mappings_from_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'a.dropdown-item:nth-child(2)')
            download_mappings_from_dropdown.click()
            os.chdir(DOWNLOAD_DIR_PATH)
            # assert file downloaded then remove it
            for file in os.listdir(os.curdir):
                if file.startswith('interface_config') and file.endswith('.csv'):
                    assert file
                    path = os.path.abspath(file)
                    os.remove(path)
                elif file.startswith('ip_mapping') and file.endswith('.csv'):
                    assert file
                    path = os.path.abspath(file)
                    os.remove(path)

    def _toggle_header(self, toggle_header):
        header_checkbox = self.driver.find_element(
            By.CSS_SELECTOR, 'input[id="id_csv_header"]')
        if toggle_header and not header_checkbox.is_selected():
            header_checkbox.click()
        elif not toggle_header and header_checkbox.is_selected():
            header_checkbox.click()

    def _select_delimiter(self, delimiter):
        if delimiter:
            select_delimiter_popup = Select(self.driver.find_element(By.CSS_SELECTOR, '#id_csv_delimiter'))
            select_delimiter_popup.select_by_value(delimiter)

    def _upload_file(self, file_path):
        select_file_control = self.driver.find_element(By.CSS_SELECTOR, '#id_csv_file')
        select_file_control.send_keys(file_path)

    def _confirm_or_cancel_upload(self, form_button):
        upload_button_popup = self.driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn.btn-primary')
        close_button_popup = self.driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn.btn-secondary')
        if form_button == "upload":
            upload_button_popup.click()
        else:
            close_button_popup.click()

    def _wait_interface_config_label_loads(self):
        wait_for_element_to_be_visible(self.driver, 5, 'a[href="/settings/interface_config/"]')

    def wait_mapping_upload_and_save_finishes(self):
        wait(self.driver, 500).until(ec.invisibility_of_element((By.CSS_SELECTOR, '#status-btn-del-pending')))

    def _wait_mapping_table_load(self):
        wait_for_element_to_be_clickable(self.driver, 5, '#table-ip-mappings > tbody > tr td .fa.fa-remove')

    def _choose_direction(self, relation):
        wait(self.driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.select2-results > ul > li')))
        dp_items = self.driver.find_elements(By.CSS_SELECTOR, 'span.select2-results > ul > li')
        if dp_items[0].is_enabled() and dp_items[1].is_enabled() and dp_items[2].is_enabled():
            if relation == 'both':
                dp_items[0].click()
            elif relation == 'outgoing':
                dp_items[1].click()
            elif relation == 'incoming':
                dp_items[2].click()

    def _verify_message(self, css_selector, expected_text):
        wait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        message = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        message_text_list = [x.strip() for x in message.text.split('.') if x]
        expected_text_list = [x.strip() for x in expected_text.split('.') if x]
        # the following if is to handle the issue of error messages being dynamic
        # this is based on the error messages having '.' in it
        if len(message_text_list) > 1:
            # print("found:", message_text_list)
            # print("expected: ", expected_text_list)
            assert message_text_list.sort() == expected_text_list.sort(), ('Extracted Text: "{}" does not match'
                                                                           ' Expected Text: "{}"'.format(message.text,
                                                                                                         expected_text))
        else:
            assert message.text == expected_text, 'Extracted Text: "{}", found: "{}" '.format(expected_text,
                                                                                              message.text)
