import time
import os
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from ..POM.BaseClass import BaseClass

from Modules.element_attributes import element_visible_and_enabled
from Modules.custom_waits import wait_for_element_to_be_clickable, wait_for_element_to_be_visible
from Data.data_path import DOWNLOAD_DIR_PATH


class KPIsReportLevel(BaseClass):
    """
    This class serves as parent class to all KPI classes.
    """

    def __init__(self, driver):
        self.driver = driver
        self.initialize_attributes()
        # print("Init Sup class {} - Report Name {}, Report ID {}".format(__class__.__name__, self.report_name,
        #                                                                 self.report_id))

    def _open(self):
        self.open_report_level()
        self._buffer_report_name()
        self._buffer_report_id()

    def initialize_attributes(self):
        """
        Used to initialize KPI specific attributes. Must be declared here, since it's used in the __ini__ of all
        derived classes. It's overriden in each derived class with own kpi specific attributes.
        """
        self.default_table_headers = []
        self.default_columns_dropdown = []
        self.csv_kpi_name = ''
        self.possible_permissions_dict = {}
        self.report_id = ''
        self.report_name = ''

    def download_kpi_as_csv(self):
        self._wait_kpi_table_load()
        export_data = self.driver.find_element(By.CSS_SELECTOR, '.export.btn-group')
        export_data.click()
        csv_download = self.driver.find_element(By.CSS_SELECTOR,
                                                'ul.dropdown-menu > li:nth-child(1) > a:nth-child(1)')
        csv_download.click()

    def reset_filters(self):
        self._open_all_filters()
        reset_all_filters_button = self.driver.find_element(By.CSS_SELECTOR, '#apply-default-filter-config')
        reset_all_filters_button.click()

    def filter_by_time_frame(self, time_frame):
        if time_frame:
            self._open_all_filters()
            time_frame_input = self.driver.find_element(By.CSS_SELECTOR, 'input#time-frame')
            time_frame_input.clear()
            time_frame_input.send_keys(time_frame, Keys.ENTER)
            self._apply_filters()

    def filter_by_start_and_end_time(self, start_time, end_time):
        if start_time or end_time:
            self._open_all_filters()
            start_time_input = self.driver.find_element(By.CSS_SELECTOR, 'input#start-time')
            end_time_input = self.driver.find_element(By.CSS_SELECTOR, 'input#end-time')
            clear_start_time = self.driver.find_element(By.CSS_SELECTOR, '#clear-start-time > span:nth-child(1)')
            clear_end_time = self.driver.find_element(By.CSS_SELECTOR, '#clear-end-time > span:nth-child(1)')
            clear_start_time.click()
            clear_end_time.click()
            start_time_input.send_keys(start_time, Keys.ENTER)
            end_time_input.send_keys(end_time, Keys.ENTER)
            self._apply_filters()

    def filter_by_kpi_boundaries(self, **boundaries):
        """
        :param boundaries: a dictionary representing boundaries and its different options, all values are str
               Example:
               {
               'kpi_lower_bound': any str representing float i.e. '2.3' ,
               'kpi_upper_bound': any str representing float i.e '10.0,
               'kpi_boundaries_kpi':'sept' |'sert' | 'seet'
               }
        """
        if not boundaries:
            return
        self._open_all_filters()
        if boundaries.get('kpi_lower_bound'):
            lower_bound = self.driver.find_element(By.CSS_SELECTOR, '#kpi-lower-bound')
            lower_bound.send_keys(boundaries.get('kpi_lower_bound'))
        if boundaries.get('kpi_upper_bound'):
            upper_bound = self.driver.find_element(By.CSS_SELECTOR, '#kpi-upper-bound')
            upper_bound.send_keys(boundaries.get('kpi_upper_bound'))
        if boundaries.get('kpi_boundaries_kpi'):
            boundaries_kpi_select = Select(self.driver.find_element(By.CSS_SELECTOR, '.kpi-boundaries-filter-select'))
            boundaries_kpi_select.select_by_value(boundaries.get('kpi_boundaries_kpi'))
        self._apply_filters()

    def filter_by_from_and_to_headers(self, from_header, to_header):
        self._open_all_filters()
        if from_header:
            from_field = self.driver.find_element(By.CSS_SELECTOR, '#header-name')
            from_field.send_keys(from_header)
        if to_header:
            to_field = self.driver.find_element(By.CSS_SELECTOR, '#header-value')
            to_field.send_keys(to_header)
        self._apply_filters()

    def filter_by_interface(self, *interfaces):
        self._open_all_filters()
        interface_field = self.driver.find_element(By.CSS_SELECTOR, 'ul.select2-selection__rendered')
        for interface in interfaces:
            interface_field.send_keys(interface)
        self._apply_filters()

    def filter_by_n_patterns(self, n_patterns):
        if not n_patterns:
            return
        self._open_all_filters()
        clear_call_pattern = self.driver.find_element(By.CSS_SELECTOR,
                                                      'div.input-group-append > .btn.btn-secondary[title="Reset call patterns"]')

        clear_call_pattern.click()
        call_pattern_filter = self.driver.find_element(By.CSS_SELECTOR, '#callPatternsFilter #selected-call-patterns')
        call_pattern_filter.click()
        for i in range(n_patterns):
            pattern_checkbox = self.driver.find_element(By.CSS_SELECTOR, '#patterns-checkbox')
            pattern_checkbox.click()
            next_pattern = self.driver.find_element(By.CSS_SELECTOR, '.fa-arrow-right')
            next_pattern.click()
        save_changes_button = self.driver.find_element(By.CSS_SELECTOR, '#patternContainer > div:nth-child(1)'
                                                                        ' > div:nth-child(1) > div:nth-child(3)'
                                                                        ' > button:nth-child(1)')
        save_changes_button.click()
        self._apply_filters()

    def filter_by_percentile_filter(self, **percentile):

        """
        :param percentile: a dictionary representing percentile and its different options, all values are str.
                 Examples:
                 {
                  'filter_percentile': any str representing integers from 0-99 ,
                  'filter_percentile_criteria': 'higher' | 'lower',
                  'filter_percentile_kpi': 'sept' | 'seet' | 'sert'
                 }
        """
        if not percentile:
            return
        self._open_all_filters()
        if percentile.get('filter_percentile'):
            percentile_combobox = self.driver.find_element(By.CSS_SELECTOR, '.select2-selection--single')
            percentile_combobox.click()
            percentile_combobox_input = self.driver.find_element(By.CSS_SELECTOR,
                                                                 'span.select2-search > input:nth-child(1)')
            percentile_combobox_input.send_keys(percentile['filter_percentile'])

        if percentile.get('filter_percentile_criteria'):
            percentile_criteria_select = Select(
                self.driver.find_element(By.CSS_SELECTOR, 'select.custom-select:nth-child(1)'))
            percentile_criteria_select.select_by_value(percentile.get('filter_percentile_criteria'))
        if percentile.get('filter_percentile_kpi'):
            percentile_kpi_select = Select(self.driver.find_element(By.CSS_SELECTOR, '.kpi-select'))
            percentile_kpi_select.select_by_value(percentile.get('filter_percentile_kpi'))
        self._apply_filters()

    def compare_csv(self, path_to_csv_with_verified_values, path_to_downloaded_file=None):

        """
        compares a downloaded CSV (saved in Data -> Downloads -> filename)
        with an already saved CSV that has the expected values.

        :param path_to_csv_with_verified_values: str this is the path to the CSV file that has the expected and right
        values.
        :param path_to_downloaded_file: str this is the path to the downloaded CSV, if none is given, then the
        downloaded file is a KPI csv file that has different naming than a mos csv naming.
        """
        errors_list = list()
        # if path_to_downloaded_file is None, then the call to this function was made to verify KPIs CSV, otherwise MOS
        if not path_to_downloaded_file:
            path_to_downloaded_file = DOWNLOAD_DIR_PATH + self._get_csv_name()

        try:
            with open(path_to_csv_with_verified_values, encoding='utf-8') as verified_file:
                verified_csv = csv.reader(verified_file, delimiter=',')
                verified_list = [row for row in verified_csv]
            with open(path_to_downloaded_file, encoding='utf-8') as downloaded_file:
                downloaded_csv = csv.reader(downloaded_file, delimiter=',')
                downloaded_list = [row for row in downloaded_csv]
        except Exception as e:
            errors_list.append(e)
        if len(verified_list) != len(downloaded_list):
            errors_list.append(
                ' Rows count mistmacthes! downloaded CSV from Report: "{}" - KPI {} has {} lines, verified CSV has {} '
                'lines'.format(self.report_id, self.csv_kpi_name, len(downloaded_list), len(verified_list))
            )
            raise Exception(errors_list)
        for row in verified_list:
            if row not in downloaded_list:
                errors_list.append(
                    ' Row Nr.{} in verified file not found in downloaded file from Report: "{}" - KPI {}'.format(
                        verified_list.index(row), self.report_id, self.__class__.__name__)
                )
        if errors_list:
            # print('*****', errors_list)
            # print('len: ', len(errors_list))
            raise Exception(errors_list)
        self._verify_file_downloaded_and_delete_file(path_to_downloaded_file.split('/')[-1])

    def _buffer_report_id(self):
        breadcrumb_navigation_report = self.driver.find_element(By.CSS_SELECTOR,
                                                                'li.breadcrumb-item:nth-child(3) > a:nth-child(1)').text
        self.report_id = breadcrumb_navigation_report.split('#')[-1]

    def _buffer_report_name(self):
        toggle_header = self.driver.find_element(By.CSS_SELECTOR, '.toggle-details')
        self.report_name = toggle_header.text

    def _buffer_call_id(self):
        breadcrum_navigation_call = self.driver.find_element(By.CSS_SELECTOR,
                                                             'li.breadcrumb-item:nth-child(5) > a:nth-child(1)').text
        self.call_id = breadcrum_navigation_call.split('#')[-1]

    def _get_csv_name(self):
        # if call level kpi is open, then call_id can be seen and this can be used to construct csv name")
        if element_visible_and_enabled(self.driver, 'li.breadcrumb-item:nth-child(5) > a:nth-child(1)'):
            self._buffer_call_id()
            csv_name = ('report_' + self.report_id + '_' + self.report_name + '_call_' + self.call_id + '_'
                        + self.csv_kpi_name + '.csv')
            return csv_name
        else:
            csv_name = 'report_' + self.report_id + '_' + self.report_name + '_' + self.csv_kpi_name + '.csv'
            return csv_name

    # TODO: move to KPISsCallLevel maybe? and other similar methods used there only?
    def open_call_level(self):
        """
        This method switches to call level. It tries to find the Call ID in breadcrumb, if not found, that means
        call level isn't opened, so it opens call level, by selecting the first call in "All Calls" Tabel
        """
        if not element_visible_and_enabled(self.driver, 'li.breadcrumb-item:nth-child(5) > a:nth-child(1)'):
            # open all calls table
            all_calls = self.driver.find_element(By.CSS_SELECTOR, 'ul > li[title="All Calls"] > a')
            all_calls.click()
            wait_for_element_to_be_clickable(self.driver, 5, '.fa-list-alt')
            open_call_level_from_all_calls = self.driver.find_element(By.CSS_SELECTOR, '.fa-list-alt')
            open_call_level_from_all_calls.click()

    def open_report_level(self):
        """
        This method switches to report level. It tries to find the Call ID in breadcrumb, if found, that means
        report level isn't opened, so it opens report level, by changing url to report level url
        """
        # if the Call ID is visible in the breadcrumb, then you're on call level, so switch to report level
        if element_visible_and_enabled(self.driver, 'li.breadcrumb-item:nth-child(5) > a:nth-child(1)'):
            report_level_url = self.driver.current_url.split('call')[0]
            self.driver.get(report_level_url)

    def verify_default_headers_ordered_in_table_and_dropdown(self):
        self._wait_kpi_table_load()
        header_objects = self.driver.find_elements(By.CSS_SELECTOR, '.seta-datatable > thead > tr > th')
        header_objects_text = [x.text for x in header_objects]
        assert header_objects_text == self.default_table_headers, '{} : Mismatching Headers. Expected {}, found {}'.format(
            self.__class__.__name__, self.default_table_headers, header_objects_text)

    def verify_permissions(self, allowed_permissions_list):
        """
        This function takes a dictionary key that specifies what permissions/columns in KPI should be visible
        and verifies that. It also considers all other permissions/columns not passed to it as a restriction
        and verifies that these permissions/columns are not visible in the KPI.

        :param allowed_permissions_list:  Dictionary key used with Class Dictionary attribute to specify the
        allowed columns in the KPI.
        """
        self._wait_kpi_table_load()
        if allowed_permissions_list == self.possible_permissions_dict['All  Permissions']:
            self.verify_default_headers_ordered_in_table_and_dropdown()
        else:
            self._verify_viewing_permissions(allowed_permissions_list)
            self._verify_viewing_restrictions(allowed_permissions_list)

    # TODO: should I verify that all table headers other permissions related are correctly visbile in this function too?
    def _verify_viewing_permissions(self, allowed_permissions_list):
        self._open_table_columns_dropdown()
        dropdown_objects = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu-right > .dropdown-item')
        dropdown_objects_text = [x.text for x in dropdown_objects]
        header_objects = self.driver.find_elements(By.CSS_SELECTOR, '.seta-datatable > thead > tr > th')
        header_objects_text = [x.text for x in header_objects]
        # loop through allowed_permission_list and make sure each element is found in the header_objects_text and is enabled in Dropdown.
        for permission in allowed_permissions_list:
            if permission not in header_objects_text:
                raise AssertionError(f'Allowed Permission {permission} not found in Table Header!')
            else:
                permission_index_in_drop_down = dropdown_objects_text.index(permission)
                enabled_checkbox = dropdown_objects[permission_index_in_drop_down].find_element(By.CSS_SELECTOR,
                                                                                                'input')
                assert enabled_checkbox.is_enabled(), 'Header:{} checkbox is not enabled in dropdown'.format(permission)
                assert enabled_checkbox.is_selected(), 'Header:{} checkbox is not selected in dropdown'.format(
                    permission)

    def _verify_viewing_restrictions(self, allowed_permissions_list):
        # verify restrictions are not displayed in table
        dropdown_objects = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu-right > .dropdown-item')
        dropdown_objects_text = [x.text for x in dropdown_objects]
        header_objects = self.driver.find_elements(By.CSS_SELECTOR, '.seta-datatable > thead > tr > th')
        header_objects_text = [x.text for x in header_objects]
        # get the denied cols/restricted by removing the allowed cols from the total of
        # all possible restrictions
        denied_permissions = self.possible_permissions_dict['All  Permissions'].copy()
        [denied_permissions.remove(permission) for permission in allowed_permissions_list]
        for restriction in denied_permissions:
            if restriction in header_objects_text:
                raise AssertionError(
                    f'in KPI {self.__class__.__name__} Restricted Col: {restriction} found in Table Header!')
            else:
                restriction_index_in_drop_down = dropdown_objects_text.index(restriction)
                disabled_checkbox = dropdown_objects[restriction_index_in_drop_down].find_element(By.CSS_SELECTOR,
                                                                                                  'input')
                # assert that the permission in Dropdown can be selected(enabled) and is selected
                assert disabled_checkbox.is_enabled() is True
                assert disabled_checkbox.is_selected() is False

    # Using hard coded table headers passed to function from any report object
    # make sure that these header are : 1. Either availabe completely 2.if not available, then they must be restricted
    # and thus verify they're restricted in dropdown 3. if neither of 1 or 2, then there's an error
    def _verify_header_exist_or_restricted(self, headers=None, dropdown_items_p=None):
        table_headers = self.driver.find_elements(By.CSS_SELECTOR,
                                                  '.fixed-table-body > table.table-striped > thead > tr > th')
        table_headers_list = [x.text for x in table_headers]
        dropdown_items = dropdown_items_p
        dropdown_items_list = [x.text for x in dropdown_items]
        if headers is not None:
            for head in headers:
                if head in table_headers_list:
                    # print(f'Head {head} is in table headers')
                    continue
                elif head not in table_headers_list:
                    # print(f'Head {head} is not in table headers')
                    assert head in dropdown_items_list
                    dropdown_item = dropdown_items[dropdown_items_list.index(head)]
                    assert dropdown_item.find_element(By.CSS_SELECTOR, 'input').is_selected() is False
                    # print(f'Head {head} is not in table headers, because restricted')
                else:
                    raise AssertionError(f'There are headers like {head} not detected in Table header or Dropdown Menu')

    def _wait_kpi_table_load(self):
        time.sleep(1)
        cell = self.driver.find_elements(By.CSS_SELECTOR, '.seta-datatable > tbody tr td')
        if 'no matching records found' not in cell[0].text.lower():
            return
        else:
            time.sleep(3)

    def _open_table_columns_dropdown(self):
        open_dropdown = self.driver.find_element(By.CSS_SELECTOR, '.keep-open > button:nth-child(1)')
        open_dropdown.click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu-right')
        return dropdown

    # TODO: This method should be statics because it's not accessing any of the class attributes.
    def _verify_file_downloaded_and_delete_file(self, filename):
        os.chdir(DOWNLOAD_DIR_PATH)
        assert filename in os.listdir(os.path.abspath(os.curdir)), 'File: {} was not downloaded!'.format(filename)
        os.remove(filename)

    def _open_all_filters(self):
        filters_button = self.driver.find_element(By.CSS_SELECTOR, '.filter-button')
        if filters_button.get_attribute('aria-expanded') == 'false':
            filters_button.click()

    def _apply_filters(self):
        submit_all_filters_button = self.driver.find_element(By.CSS_SELECTOR, '#submit-filter-config')
        submit_all_filters_button.click()

    """Merging SingleReport to KPIsReportLevel"""

    def verify_edit_report_enabled(self):
        self._open_actions_menu_if_not_opened()
        edit_report = self.driver.find_element(By.CSS_SELECTOR, 'a.dropdown-item:nth-child(9)')
        assert edit_report.is_enabled(), 'Edit Report is disabled!'

    def verify_delete_report_enabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#delete-report')
        assert dropdown_item.is_enabled(), 'Delete Report is disabled!'

    def verify_download_merged_pcaps_disabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-item:nth-child(1)')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Download Merged PCAPs is enabled!'

    def verify_download_original_pcap_disabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-item:nth-child(2)')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Download Original PCAP is enabled!'

    def verify_edit_report_disabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-item:nth-child(7)')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Edit Report is enabled!'

    def verify_delete_report_disabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#delete-report')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Delete Report is enabled!'

    def verify_download_merged_pcap_enabed_and_download_works(self):
        report_name = 'report_' + self.report_id + '.pcapng'
        self._open_actions_menu_if_not_opened()
        self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-menu > a:nth-child(1)').click()
        self._verify_file_downloaded_and_delete_file(report_name)

    def verify_download_original_pcaps_enabed_and_download_works(self):
        report_name = 'report_' + self.report_id + '.zip'
        self._open_actions_menu_if_not_opened()
        self.driver.find_element(By.CSS_SELECTOR, 'a.dropdown-item:nth-child(2)').click()
        self._verify_file_downloaded_and_delete_file(report_name)

    def verify_mos_file_upload_enabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#upload-mos-file')
        assert dropdown_item.is_enabled(), 'Upload MOS file is disabled!'

    def verify_mos_file_download_enabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#download-mos-file')
        assert dropdown_item.is_enabled(), 'Download MOS file is disabled!'

    def verify_mos_file_upload_disabled(self):
        self._open_actions_menu_if_not_opened()

        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-item:nth-child(6)')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Upload MOS file is enabled!'

    def verify_mos_file_download_disabled(self):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR,
                                                 'div.dropdown-item:nth-child(7)')
        assert dropdown_item.get_attribute('class') == 'dropdown-item disabled', 'Download MOS file is enabled!'

    def upload_mos_file_verify_upload_message(self, mos_file_path, delimiter=None, expected_message=None,
                                              form_button='upload'):
        self._open_actions_menu_if_not_opened()
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#upload-mos-file')
        dropdown_item.click()
        self._select_delimiter(delimiter)
        self._upload_file(mos_file_path)
        self._confirm_or_cancel_upload(form_button)
        if expected_message:
            wait_for_element_to_be_visible(self.driver, 5, '.alert')
            found_message = self.driver.find_element(By.CSS_SELECTOR, '.alert').text
            assert expected_message == found_message, 'Expected Message is "{}", found "{}"'.format(expected_message,
                                                                                                    found_message)

    def download_mos_file_verify_download(self, verified_mos_file):
        self._open_actions_menu_if_not_opened()
        self.driver.find_element(By.CSS_SELECTOR, '#download-mos-file').click()
        # split to get only 'filename.csv', then split again to get only 'filename'
        csv_name = verified_mos_file.split('/')[-1].split('.')[0]
        downloaded_csv = self._find_file_in_given_directory(DOWNLOAD_DIR_PATH, csv_name)
        # self.compare_csv(mos_file_name, download_dir + csv_name)
        # print('-> verified mos csv: ', verified_mos_file)
        # print('-> downloaded mos csv: ', downloaded_csv)
        self.compare_csv(verified_mos_file, downloaded_csv)

    def _find_file_in_given_directory(self, directory_path, filename_starts_with):
        os.chdir(directory_path)
        # print('->curdir path: ', os.path.abspath(directory_path))
        # print('->name starts with: ', filename_starts_with)
        files_objects = [x for x in os.scandir(os.curdir) if x.name.startswith(filename_starts_with)]
        # sort file object ascnedingly according to creation time, the lowest is oldest, highest is newest
        files_objects.sort(key=lambda entry: entry.stat().st_mtime)
        file_path = files_objects[-1].path
        # print('->file_path: ', file_path)
        return os.path.abspath(file_path)

    def _click_edit_report(self): #
        edit_report = self.driver.find_element(By.CSS_SELECTOR, 'a.dropdown-item:nth-child(9)')
        edit_report.click()

    def _fill_description_field(self, description):
        description_field = self.driver.find_element(By.CSS_SELECTOR, '#id_description')
        description_field.clear()
        description_field.send_keys(description, Keys.TAB)

    def _fill_users_field(self, users_list):
        if users_list:
            for user in users_list:
                users_field = self.driver.find_element(By.CSS_SELECTOR,
                                                       'div.form-group:nth-child(3) > .col-md-9'
                                                       ' > span.select2.select2-container'
                                                       ' ul.select2-selection__rendered > li.select2-search > input')
                users_field.clear()
                users_field.send_keys(Keys.ENTER)
                users_field.send_keys(user, Keys.ENTER)

    def _fill_groups_fied(self, groups_list):
        if groups_list:
            for group in groups_list:
                groups_field = self.driver.find_element(By.CSS_SELECTOR,
                                                        'div.form-group:nth-child(4) > .col-md-9'
                                                        ' > span.select2.select2-container'
                                                        ' ul.select2-selection__rendered > li.select2-search > input')
                groups_field.clear()
                groups_field.send_keys(Keys.ENTER)
                groups_field.send_keys(group, Keys.ENTER)

    def edit_report(self, description='', users_list=None, groups_list=None):
        self._open_actions_menu_if_not_opened()
        self._click_edit_report()
        self._fill_description_field(description)
        self._clear_groups_users_fields_edit_report(users_list, groups_list)
        self._fill_users_field(users_list)
        self._fill_groups_fied(groups_list)
        update = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        update.click()

    def delete_report(self):
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#delete-report')
        if not dropdown_item.is_displayed():
            dropdown_menu = self.driver.find_element(By.CSS_SELECTOR, '#dropdownMenuButton')
            dropdown_menu.click()
            dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#delete-report')
            dropdown_item.click()
        else:
            dropdown_item.click()

    def confirm_delete_report(self):
        wait_for_element_to_be_visible(self.driver, 10, '#reportDeleteConfirmModal')
        # wait(self.driver, 10).until(EC.visibility_of_element_located(
        #     (By.CSS_SELECTOR, '#reportDeleteConfirmModal')))
        delete_btn = self.driver.find_element(By.CSS_SELECTOR, '#confirm-delete-button')
        delete_btn.click()

    def _verify_file_downloaded_and_delete_file(self, filename):
        os.chdir(DOWNLOAD_DIR_PATH)
        assert filename in os.listdir(), 'File: {} was not downloaded!'.format(filename)
        os.remove(filename)

    def _clear_groups_field_edit_report(self):
        clear_groups_field = self.driver.find_elements(By.CSS_SELECTOR,
                                                       'div.form-group:nth-child(4) > .col-md-9'
                                                       ' > span.select2.select2-container'
                                                       ' ul.select2-selection__rendered'
                                                       ' > li.select2-selection__choice > span')
        groups_count = len(clear_groups_field)
        for i in groups_count:
            clear_groups_field = self.driver.find_elements(By.CSS_SELECTOR,
                                                           'div.form-group:nth-child(4)'
                                                           ' > .col-md-9 > span.select2.select2-container'
                                                           ' ul.select2-selection__rendered'
                                                           '> li.select2-selection__choice > span')
            clear_groups_field[i].click()
            groups_field = self.driver.find_element(By.CSS_SELECTOR,
                                                    'div.form-group:nth-child(4) > .col-md-9'
                                                    ' > span.select2.select2-container'
                                                    ' ul.select2-selection__rendered > li.select2-search > input')
            groups_field.click()
            groups_field.send_keys(Keys.TAB)

    def _clear_users_field_edit_report(self):
        clear_users_field = self.driver.find_elements(By.CSS_SELECTOR,
                                                      'div.form-group:nth-child(3) > .col-md-9'
                                                      ' > span.select2.select2-container'
                                                      ' ul.select2-selection__rendered'
                                                      ' > li.select2-selection__choice > span')
        users_count = len(clear_users_field)
        for i in range(users_count):
            clear_users_field = self.driver.find_elements(By.CSS_SELECTOR,
                                                          'div.form-group:nth-child(3) > .col-md-9'
                                                          ' > span.select2.select2-container'
                                                          ' ul.select2-selection__rendered'
                                                          ' > li.select2-selection__choice > span')
            clear_users_field[i].click()
            users_field = self.driver.find_element(By.CSS_SELECTOR,
                                                   'div.form-group:nth-child(3) > .col-md-9'
                                                   ' > span.select2.select2-container'
                                                   ' ul.select2-selection__rendered > li.select2-search > input')
            users_field.click()
            users_field.send_keys(Keys.TAB)

    def _clear_groups_users_fields_edit_report(self, users, groups):
        if groups:
            self._clear_groups_field_edit_report()
        if users:
            self._clear_users_field_edit_report()

    def _open_actions_menu_if_not_opened(self):
        time.sleep(.5)
        dropdown_item = self.driver.find_element(By.CSS_SELECTOR, '#dropdownMenuButton')
        if dropdown_item.get_attribute('aria-expanded') == 'false':
            dropdown_item.click()

    def _buffer_report_id(self):
        breadcrum_navigation_report = self.driver.find_element(By.CSS_SELECTOR,
                                                               'li.breadcrumb-item:nth-child(3) > a:nth-child(1)').text
        self.report_id = breadcrum_navigation_report.split('#')[1]

    def _buffer_report_name(self):
        toggle_header = self.driver.find_element(By.CSS_SELECTOR, '.toggle-details')
        self.report_name = toggle_header.text

    def _buffer_call_id(self):
        breadcrum_navigation_call = self.driver.find_element(By.CSS_SELECTOR,
                                                             'li.breadcrumb-item:nth-child(5) > a:nth-child(1)').text
        self.call_id = breadcrum_navigation_call.split('#')[1]

    def _select_delimiter(self, delimiter):
        if delimiter:
            select_delimiter_popup = Select(self.driver.find_element(By.CSS_SELECTOR, '#id_csv_delimiter'))
            select_delimiter_popup.select_by_value(delimiter)

    def _upload_file(self, file_path):
        select_file_control = self.driver.find_element(By.CSS_SELECTOR, '#id_mos_file')
        select_file_control.send_keys(file_path)

    def _confirm_or_cancel_upload(self, form_button):
        upload_button_popup = self.driver.find_element(By.CSS_SELECTOR, '#submit-mos-csv-file-button')
        close_button_popup = self.driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn.btn-secondary')
        if form_button == "upload":
            upload_button_popup.click()
        else:
            close_button_popup.click()
