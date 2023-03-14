from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from .BaseClass import BaseClass
from Modules.element_attributes import element_exists_within_object
from Modules.custom_waits import wait_for_element_to_be_invisible


class CreateReport(BaseClass):

    def __init__(self, driver):
        super().__init__(driver)

    def fill_report_form_by_form_number(self, pcaps_list=None, anonymize_report=None, description=None,
                                        report_form_number=1, username=None,
                                        groupname=None):
        """
        This function allows you to choose a specific report form to fill in with PCAPs, Description, Users, Groups and
        anonymize option. The first Form/report Number is 1, to add another form/report, use add_report_button() first

        :param pcaps_list: list(str) of paths to PCAP files.
        :param anonymize_report: bool to mark or unmark the anonymize option checkbox
        :param description: str the report's name
        :param report_form_number: int the report's/form's number to enter parameters into
        :param username: str the name of the user to share this report with
        :param groupname: str the name of the group to share this report with
        """

        report_form_number = '#new-report-form-' + str(report_form_number - 1)
        report_form = self.driver.find_element(By.CSS_SELECTOR, report_form_number)
        if pcaps_list:
            for file in pcaps_list:
                self._upload_file_single(report_form, file)
        self._anonymize(report_form, anonymize_report)
        self._fill_description(report_form, description)
        self._fill_users(report_form, username)
        self._fill_groups(report_form, groupname)

    # TODO: documentation
    def fill_bulk_reports_forms(self, anonymize_reports_list=None, descriptions_list=None, users_list=None,
                                groups_list=None, pcaps_list=None):
        if pcaps_list:
            self._bulk_upload_files_to_all_forms(pcaps_list)
        reports_forms = self.driver.find_elements(
            By.CSS_SELECTOR, '#new-reports-container > li')
        for report_form in reports_forms[1:]:
            if anonymize_reports_list:
                # the -1 is due to additional li element in the end, that's not visible.
                self._anonymize(report_form, anonymize_reports_list[reports_forms.index(report_form) - 1])
            if descriptions_list:
                self._fill_description(report_form, descriptions_list[reports_forms.index(report_form) - 1])
            if users_list:
                self._fill_users(report_form, users_list[reports_forms.index(report_form) - 1])
            if groups_list:
                self._fill_groups(report_form, descriptions_list[reports_forms.index(report_form) - 1])

    def upload_file_to_specific_form(self, form_number=1, pcaps_list=None):
        form_number -= 1
        self.driver.execute_script("$('#bulk-upload-container').removeClass('d-none')")
        browse = self.driver.find_element(By.CSS_SELECTOR, '#id_form-' + str(form_number) + '-pcaps')
        for pcap in pcaps_list:
            browse.send_keys(pcap)

    def _bulk_upload_files_to_all_forms(self, pcaps_list):
        for count in range(len(pcaps_list)):
            self.driver.execute_script("$('#bulk-upload-container').removeClass('d-none')")
            self.driver.execute_script(
                "$('#bulk-upload-container').append('<input id=\"id_inp-bulk-upload-" + str(
                    count) + "\" name=\"inp-bulk-upload-" + str(
                    count) + "\" class=\"inp-bulk-upload\" type=\"file\" multiple/>')")
            wait(self.driver, 5).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '#id_inp-bulk-upload-' + str(count))))
            browse = self.driver.find_element(By.CSS_SELECTOR, '#id_inp-bulk-upload-' + str(count))
            browse.send_keys(pcaps_list[count])

    def verify_still_on_same_view(self):
        header = self.driver.find_element(By.CSS_SELECTOR, '#content')
        assert header.text == 'New Report(s)', 'Not on Report(s) view'

    def verify_message_size_over_50mb(self):
        alert_message = self.driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger')
        assert alert_message.text == '×\nPlease keep overall file size under 50.0 MB. Current filesize 114.8 MB', (
            'Exceeding pcap size error mistmaches')

    def verify_message_size_over_50mb_bulk(self):
        report_forms = self.driver.find_elements(By.CSS_SELECTOR, 'li.report-form-list-item')
        for form in report_forms:
            if form.get_attribute('class') != 'report-form-list-item new-report-form d-none':
                if element_exists_within_object(form, '.alert.alert-danger'):
                    alert_message = form.find_element(By.CSS_SELECTOR, '.alert.alert-danger')
                    assert alert_message.text == ('×\nPlease keep overall file size under 50.0 MB.'
                                                  ' Current filesize 114.8 MB'), ('Exceeding pcap size error'
                                                                                  ' mistmaches')

    def verify_anonymized_disabled_label_appear(self):
        anonymize_chkbx = self.driver.find_element(By.CSS_SELECTOR, '#id_form-0-is_anonymized')
        assert not anonymize_chkbx.is_enabled(), 'Anonymize Report checkbox is enabled!'
        anonymize_label = self.driver.find_element(By.CSS_SELECTOR, '.form-check-label')
        assert anonymize_label.text == 'Anonymize Report (no permission to create non-anonymized report)', (
            'Anonymize Repor Label Text mismatches')

    def verify_anonymized_enabled_click_unclick_checkbox(self):
        anonymize_chkbx = self.driver.find_element(By.CSS_SELECTOR, '#id_form-0-is_anonymized')
        assert anonymize_chkbx.is_enabled(), 'Anonymize Report checkbox is disabled!'
        if anonymize_chkbx.is_selected():
            anonymize_chkbx.click()
            assert not anonymize_chkbx.is_selected(), 'Anonymize Report checkbox is selected!'
        elif not anonymize_chkbx.is_selected:
            anonymize_chkbx.click()
            assert anonymize_chkbx.is_selected(), 'Anonymize Report checkbox is not selected!'

    def wait_upload_modal_disappears(self):
        wait_for_element_to_be_invisible(self.driver, 600, '#pleaseWaitDialog')

    def add_report_button(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '#btn-add-report')
        btn.click()

    def create_report_button(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '#btn-pcap-form-submit')
        btn.click()

    def reset_forms_button(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-danger')
        btn.click()

    def _upload_file_single(self, report_form, pcap_file_path):
        pcap_field = report_form.find_element(By.CSS_SELECTOR, 'li > div:nth-child(1) input')
        pcap_field.send_keys(pcap_file_path)

    def _fill_description(self, report_form, description):
        if description:
            description_field = report_form.find_element(By.CSS_SELECTOR, 'li > div:nth-child(3) input')
            if description == 'clear':
                description_field.clear()
            else:
                description_field.clear()
                description_field.send_keys(description, Keys.TAB)

    def _fill_users(self, report_form, username):
        if username:
            users_field = report_form.find_element(By.CSS_SELECTOR,
                                                   'li > div.form-group:nth-child(4) > div > span input')
            users_field.send_keys(username, Keys.ENTER)
            users_field.send_keys(Keys.TAB)

    def _fill_groups(self, report_form, groupname):
        if groupname:
            groups_field = report_form.find_element(
                By.CSS_SELECTOR, 'li > div:nth-child(5) input')
            groups_field.send_keys(groupname, Keys.ENTER)
            groups_field.send_keys(Keys.TAB)

    def _anonymize(self, report_form, anonymize_report):
        """
        This function follow the natural behaviour of SETA, where the default behaviour for the 'Anonymize Report'
        checkbox is to be selected in all cases. If Report should be not-anonymized, the function asserts that the
        checkbox is enabled (can be checked/unchecked). Otherwise if a Report should be anonymized, the function
        will just assert the checkbox is selected
        :param report_form: in which form number is the checkbox
        :param anonymize_report: (bool) if True check "Annymize Report", else-> False
        """
        anonymize_chkbox = report_form.find_element(
            By.CSS_SELECTOR, 'li > div:nth-child(2) input')
        if not anonymize_report:
            assert anonymize_chkbox.is_enabled(), (
                'Anonymize Report Checkbox is greyed out. Make sure user/group has permission')
            anonymize_chkbox.click()
            assert not anonymize_chkbox.is_selected(), (
                'Anonymized Report Checkbox could not be unselected. Make sure user/group has permission')
        else:
            assert anonymize_chkbox.is_selected()
