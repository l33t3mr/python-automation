import unittest
import time

from Modules import login, logout
from Modules.authorization_info import superuser, superuser_password, url
from Modules.shared_objects import create_create_reports_view, create_reports_view, create_firefox_driver
from Modules.helpers import create_report, create_reports, open_report, delete_report

from Data.data_path import TEST9_WIRESHARK_FILTERED_PCAP, TEST5_ADVANCED_PACP, TEST6_ADVANCED_PCAP, RANDOM_CSV


class CreateNewReports(unittest.TestCase):
    def setUp(self):
        self.driver = create_firefox_driver(url, __name__)
        self.reports_view = create_reports_view(self.driver)
        self.create_reports_view = create_create_reports_view(self.driver)
        login.login(self.driver, superuser, superuser_password)

    def tearDown(self):
        time.sleep(2)
        logout.logout(self.driver)
        self.driver.quit()

    def test_1(self):  # TCST-282 : New Report PCAP Size Limit Single File
        create_report(self.reports_view, self.create_reports_view, [TEST9_WIRESHARK_FILTERED_PCAP],
                      False, 'Test1')
        self.create_reports_view.verify_message_size_over_50mb()

    def test_2(self):  # TCST-281 : New Report PCAP Size Limit (Bulk Upload)
        create_reports(self.reports_view, self.create_reports_view,
                       pcaps_list=[TEST9_WIRESHARK_FILTERED_PCAP, TEST5_ADVANCED_PACP, TEST6_ADVANCED_PCAP])
        self.create_reports_view.verify_message_size_over_50mb_bulk()

    def test_3(self):  # TCST-16 : Can't Create Report With Non-pcap Files
        create_report(self.reports_view, self.create_reports_view, pcaps_list=[RANDOM_CSV])
        self.create_reports_view.verify_still_on_same_view()

    def test_5(self):  # TCST-538 : Create Multiple Reports with Bulk Upload
        create_reports(self.reports_view, self.create_reports_view,
                       pcaps_list=[TEST5_ADVANCED_PACP, TEST6_ADVANCED_PCAP], descriptions_list=['Test5_1', 'Test5_2'])
        for report_name in ['Test5_1', 'Test5_2']:
            open_report(self.reports_view, report_name)
            delete_report(self.reports_view, report_name)

    def test_6(self):  # TCST-539 : Can't Create Empty Report
        create_report(self.reports_view, self.create_reports_view)
        self.create_reports_view.verify_still_on_same_view()


if __name__ == '__main__':
    unittest.main()
