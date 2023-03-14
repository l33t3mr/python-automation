from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from .InterfaceConfig import InterfaceConfig
from Modules.element_attributes import element_visible_and_enabled


class IpMappings(InterfaceConfig):

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        settings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/"]')
        settings.click()
        ip_mappings = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/ip_mappings/"]')
        ip_mappings.click()

    def add_entries(self, list_of_entries_tuples):
        """Will add entries entered as a list of tuples(node_name, ims_entity,ip_addr)"""
        self.wait_for_add_entry_table_to_load()
        rows_count = len(list_of_entries_tuples)
        # Loop through Add Entries table and click the + to add rows
        for row in range(rows_count - 1):
            self.driver.find_element(
                By.CSS_SELECTOR,
                '#table-new-mapping tbody > tr > td .fa.fa-plus').click()
        # extract all rows in the mappings table 'tr' elements
        rows = self.driver.find_elements(
            By.CSS_SELECTOR, '#table-new-mapping tbody tr')
        # Loop through the new rows in Add Entries table and add data
        for index in range(rows_count):
            node_name, ims_entity, ip_addr = rows[index].find_elements(By.CSS_SELECTOR, 'input')
            # send data to field
            node_name.send_keys(list_of_entries_tuples[index][0])
            ims_entity.send_keys(list_of_entries_tuples[index][1])
            ip_addr.send_keys(list_of_entries_tuples[index][2])
        add_node = self.driver.find_element(
            By.CSS_SELECTOR, '#new-mapping-form .btn.btn-primary')
        add_node.click()

    def delete_entries(self, list_of_entries_tuples):
        for entry in list_of_entries_tuples:
            search = self.driver.find_element(By.CSS_SELECTOR, '.float-right.search > input')
            # search using ip address as it's unique
            search.send_keys(entry[2].lower(), Keys.ENTER)
            self._wait_mapping_table_load()
            # Using sleep as the search is too slow and makes the wait refer to wrong element
            row_remove = self.driver.find_element(
                By.CSS_SELECTOR, '#table-ip-mappings > tbody > tr td .fa.fa-remove')
            row_remove.click()
            search.clear()

    def bulk_delete_verify_deleted(self, list_of_entries_tuples):
        self.add_entries(list_of_entries_tuples)
        self.jump_to_last_page()
        self._wait_mapping_table_load()
        table_rows = self.driver.find_elements(
            By.CSS_SELECTOR, '#table-ip-mappings > tbody tr')
        for row in table_rows:
            cell = row.find_elements(By.CSS_SELECTOR, 'td')
            cell_checkbox = row.find_element(By.CSS_SELECTOR, 'input')
            for entry in list_of_entries_tuples:
                if cell[3].text == entry[2]:
                    cell_checkbox.click()
                    break
        delete_button = self.driver.find_element(By.CSS_SELECTOR, '#btn-delete-mappings')
        delete_button.send_keys(Keys.ENTER)
        self._wait_mapping_table_load()
        self.verify_deleted(list_of_entries_tuples)

    def jump_to_last_page(self):
        if element_visible_and_enabled(self.driver, '.page-last > a'):
            show_table_last_page = self.driver.find_element(By.CSS_SELECTOR, '.page-last > a')
            show_table_last_page.click()

    def get_help_verify(self):
        get_help = self.driver.find_element(
            By.CSS_SELECTOR,
            'a[href="/help_text/ip_mappings/"] .fa-question-circle')
        main_window_handle = self.driver.window_handles[0]
        get_help.click()
        all_windows_handles = self.driver.window_handles
        for handle in all_windows_handles:
            if handle != main_window_handle:
                self.driver.switch_to.window(handle)
                wait(self.driver, 10).until(ec.text_to_be_present_in_element(
                    (By.TAG_NAME, 'h1'), 'IP Mappings'))
                header_csv_style = self.driver.find_element(By.TAG_NAME, 'h4')
                help_text = self.driver.find_element(By.TAG_NAME, 'p')
                mandatory = self.driver.find_element(By.TAG_NAME, 'ul')
                # assert header_ip_mapping.text == 'Interface Config'
                assert header_csv_style.text == 'CSV style for uploading IP mappings'
                assert help_text.text == ('The CSV must have the columns:\nNode name, IMS entity, IP address'
                                          '\nThe columns must be in this order! You can specify if you have a headline'
                                          ' or not.\nYou can choose between following delimiters: "," ";"\n'
                                          '\nThe mapping list must include at least the following node types:')

                assert mandatory.text == 'P-CSCF\nS-CSCF'
                self.driver.close()
        self.driver.switch_to.window(main_window_handle)
