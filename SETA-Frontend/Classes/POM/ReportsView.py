import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import StaleElementReferenceException

from .BaseClass import BaseClass

from Modules.custom_waits import wait_no_matching_records_appear_and_verify, wait_for_element_to_be_clickable


class ReportsView(BaseClass):

    def __init__(self, driver):
        super().__init__(driver)

    list_of_ordered_table_headers = ['ID', 'Actions', 'Description', 'File(s)',
                                     'Created at', 'Created by', 'Anonymized',
                                     'Status']

    def open(self):
        self._wait_reports_view_label_loads()
        reports = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/reports/"]')
        reports.click()

    def create(self):
        button = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        button.click()
        wait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'h1[id="content"]')))

    def verify_view_is_open(self):
        assert self.driver.find_element(By.CSS_SELECTOR, 'h1[id=content]').text == 'Reports'

    def select_all_reports(self):
        select_all = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > thead > tr > th input')
        if not select_all.is_selected():
            select_all.click()
        assert select_all.is_selected(), 'Failed to select all report on Report(s) View'

    def deselect_all_reports(self):
        select_all = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > thead > tr > th input')
        if select_all:
            select_all.click()
        assert not select_all.is_selected(), 'Failed to deselect all reports on Report(s) View'

    def select_top_report(self):
        top_report = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > tbody > tr > td input')
        top_report.click()
        assert top_report.is_selected(), 'Failed to select First Report in the Reports table'

    def deselect_top_report(self):
        top_report = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > tbody > tr > td input')
        top_report.click()
        assert not top_report.is_selected(), 'Failed to deselect First Report in the Reports table'

    def bulk_delete_reports_on_first_page(self, list_of_reports_description):
        self.wait_reports_entries_load()
        self._wait_for_report_processing()
        for report_description in list_of_reports_description:
            row = self._search_report(report_description)
            select_report = row.find_element(By.CSS_SELECTOR, '.bs-checkbox')
            select_report.click()
        delete_btn = self.driver.find_element(By.CSS_SELECTOR, '#btn-delete-reports')
        delete_btn.click()
        self._confirm_delete()

    def search_and_delete_report(self, report_description):
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#main .form-control')
        search_box.clear()
        search_box.send_keys(report_description, Keys.ENTER)
        self.wait_reports_entries_load()
        self._wait_for_report_processing()
        row = self._search_report(report_description)
        remove = row.find_element(By.CSS_SELECTOR, '.fa.fa-trash')
        remove.click()
        self._confirm_delete()
        search_box.clear()

    def search_and_open_report(self, report_description):
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#main .form-control')
        search_box.clear()
        search_box.send_keys(report_description, Keys.ENTER)
        self.wait_reports_entries_load()
        self._wait_for_report_processing()
        row = self._search_report(report_description)
        open_report = row.find_element(By.CSS_SELECTOR, '.fa.fa-list-alt')
        open_report.click()
        verify_report_opened = self.driver.find_element(By.CSS_SELECTOR, '.sidebar-heading')
        assert verify_report_opened.text == 'Report Statistics'

    def _confirm_delete(self):
        wait_for_element_to_be_clickable(self.driver, 5, '#reportDeleteConfirmModal')
        delete_btn = self.driver.find_element(By.CSS_SELECTOR, '#confirm-delete-button')
        delete_btn.click()

    def verify_delete_confirmation_content(self):
        wait(self.driver, 10).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '#reportDeleteConfirmModal')))
        modal_label = self.driver.find_element(By.CSS_SELECTOR, '#reportDeleteConfirmModalLabel')
        modal_body = self.driver.find_element(By.CSS_SELECTOR, '.modal-body')
        delete_btn = self.driver.find_element(By.CSS_SELECTOR, '#confirm-delete-button')
        cancel_btn = self.driver.find_element(By.CSS_SELECTOR, '.modal-footer > .btn.btn-secondary')
        modal_body_text_split = modal_body.text.split('#')[0]
        assert modal_label.text == 'Delete report?', ('Delete Confirmation Label changed.'
                                                      ' Current label is {}'.format(modal_label.text))
        assert modal_body_text_split == ('Do you really want to delete the selected report(s)?' or
                                         'Do you really want to delete report '), (
            'Delete Confirmation text changed.'
            'Current text is {}'.format(modal_body_text_split))
        assert delete_btn.text == 'Delete', 'Delete button text changed. current text is {}'.format(delete_btn.text)
        assert cancel_btn.text == 'Cancel', 'Cancel button text changed. current text is {}'.format(cancel_btn.text)

    def verify_can_not_delete_report(self, report_description):
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'input[class="form-control"]')
        search_box.clear()
        search_box.send_keys(report_description, Keys.ENTER)
        self.wait_reports_entries_load()
        reports_table = self.driver.find_element(
            By.CSS_SELECTOR, '#table-reports > tbody > tr .fa.fa-trash')
        assert reports_table.get_attribute('title') == 'Only owners and admins can delete a report'
        reports_table = self.driver.find_element(
            By.CSS_SELECTOR, '#table-reports > tbody > tr > td > input[name="btSelectItem"]')
        assert not reports_table.is_enabled()

    def verify_delete(self, list_of_reports_description):
        for report_description in list_of_reports_description:
            search_box = self.driver.find_element(By.CSS_SELECTOR, 'input[class="form-control"]')
            search_box.clear()
            self.wait_reports_entries_load()
            search_box.send_keys(report_description, Keys.ENTER)
            self._wait_no_matching_records_load()

    def verify_order_of_table_headers(self):
        table_headers = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > thead > tr > th')
        table_headers_list = [header.text for header in table_headers if not header.text == '']
        list_of_ordered_table_headers = self.list_of_ordered_table_headers
        assert list_of_ordered_table_headers == table_headers_list, 'Reports View(s) Table Headers changed/mistmached'

    def verify_ordering_by_header_asc_and_desc(self):
        # TODO: Verifies that sorting in the table asc | desc works with every table header
        # TODO: there might be a need to refactor this function to make it faster
        self.wait_reports_entries_load()
        table_headers = self.driver.find_elements(By.CSS_SELECTOR, '#table-reports > thead > tr > th')
        for header in table_headers[1:]:
            if header.text == 'Actions' or header.text == '':
                continue
            content_list = []
            header.click()
            self.wait_reports_entries_load()
            table_headers = self.driver.find_elements(By.CSS_SELECTOR, '#table-reports > thead > tr > th')
            table_body_rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-reports > tbody > tr')
            for row in table_body_rows:
                row_fields = row.find_elements(By.CSS_SELECTOR, 'td')
                col = row_fields[table_headers.index(header)]
                content_list.append(col.text)
            self._verify_sorting_helper(content_list, header)
            del content_list

    def _verify_sorting_helper(self, content_list, header):
        if content_list[0].isdigit():
            # print("list with digits")
            # print(content_list)
            self._verify_column_sorted_properly(content_list, int, header)
        else:
            # bootstrap sorting ignores the case, while python sorted doesn't, this is a workaround.
            content_list = [i.lower() for i in content_list]
            # print("list is string")
            # print(content_list)
            self._verify_column_sorted_properly(content_list, str, header)

    def _verify_column_sorted_properly(self, content_list, content_type, header):
        self.wait_reports_entries_load()
        css_class = header.find_element(By.CSS_SELECTOR, 'div')
        # print(css_class.get_attribute('class'))
        if css_class.get_attribute('class') == 'th-inner sortable both asc':
            # print("element asc")
            # print(list)
            # print(sorted(list, key = content_type))
            assert sorted(content_list, key=content_type) == content_list
        elif css_class.get_attribute('class') == 'th-inner sortable both desc':
            # print("element desc")
            # print(list)
            # print(sorted(content_list, key = content_type, reverse = True))
            assert sorted(content_list, key=content_type, reverse=True) == content_list
        else:
            raise AssertionError('Selenium could not find element.Check if CSS_Selector changed')

    def wait_reports_entries_load(self):
        wait_for_element_to_be_clickable(self.driver, 5, '.fa.fa-list-alt')

    def _search_report(self, report_description):
        reports_rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-reports > tbody > tr')
        for row in reports_rows:
            row_fields = row.find_elements(By.CSS_SELECTOR, 'td')
            if report_description == row_fields[3].text:
                return row
        raise ValueError('Could not find Report with description "{}"'.format(report_description))

    def _wait_for_report_processing(self):
        start_time = time.time()
        while True:
            try:
                rows = self.driver.find_element(By.CSS_SELECTOR, '#table-reports > tbody tr')
                row_fields = rows.find_elements(By.CSS_SELECTOR, 'td')
                status = row_fields[8].text
                if status == 'success':
                    return
            except StaleElementReferenceException:
                continue
            finally:
                end_time = time.time()
                if end_time - start_time > 650:
                    raise TimeoutError('Status did not change to "success". Current Status value is {}'.format(status))

    def _wait_no_matching_records_load(self):
        wait_no_matching_records_appear_and_verify(self.driver, 5, '#table-reports > tbody tr')

    def _wait_reports_view_label_loads(self):
        wait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/reports/"]')))
