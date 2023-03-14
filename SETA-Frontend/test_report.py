import unittest
import time

from Modules.authorization_info import url, superuser, superuser_password, adminuser, adminuser_password
from Modules.helpers import verify_kpis, upload_download_mos_verify_message_and_kpi, \
    delete_report, verify_own_report_actions, create_report, open_report, apply_filter
from Modules.shared_objects import create_reports_view, create_kpi_objects, create_create_reports_view, \
    create_firefox_driver

from Data.data_path import FIRST_CALL_PCAP, ERICSSON_ERICSSON_PCAP, MOS_CLABOR_PACP
from Data.Testdata.InterfaceConfiguration.InterfaceConfigData import TCST_381_SH
from Data.Testdata.Mos.MosData import *
from Data.Testdata.KPIs.FirstCall.FirstCallData import *
from Data.Testdata.Filters.Filters import start_end_callpattern_filter_dict
from Modules import login, logout


class ViewReportAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = create_firefox_driver(url, __name__)
        cls.reports_view = create_reports_view(cls.driver)
        cls.kpis_objects = create_kpi_objects(cls.driver)
        cls.all_calls = cls.kpis_objects['Report Level']['AllCalls']
        cls.create_reports_view = create_create_reports_view(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def tearDown(self):
        time.sleep(2)  # sleep time in seconds
        logout.logout(self.driver)

    # TCST-9 is covered in other TCS

    '''Report ->  Non-Anonymized Report -> 1st Report  *All TCSTS THERE*'''

    def test_1(self):  # TCST-118 to TCST-427
        login.login(self.driver, superuser, superuser_password)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      '1st_call_analyze_kpis')
        open_report(self.reports_view, '1st_call_analyze_kpis')
        verify_kpis(self.kpis_objects, non_anonymized_dict)  # Bug Ticket ST-1030/ST-1031/ST-912
        delete_report(self.reports_view, '1st_call_analyze_kpis')

    '''Report ->  Anonymized Report -> 1st Report  *All TCSTS THERE*'''

    def test_2(self):  # TCST-118 to TCST-427
        login.login(self.driver, superuser, superuser_password)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], True,
                      '1st_call_analyze_kpis_anonymized')
        open_report(self.reports_view, '1st_call_analyze_kpis_anonymized')
        verify_kpis(self.kpis_objects, anonymized_dict)  # Bug Ticket ST-1030/ST-1031/ST-912
        delete_report(self.reports_view, '1st_call_analyze_kpis_anonymized')

    '''Report ->  Filters'''

    # TODO: use 1st_call + Ericsson_Ericsson and then filter for fist call only with start-end time and verify that
    def test_3(self):  # TCST-513 : Testing Call Pattern/Start time - End time
        login.login(self.driver, superuser, superuser_password)
        create_report(self.reports_view, self.create_reports_view,
                      [FIRST_CALL_PCAP, ERICSSON_ERICSSON_PCAP], False,
                      'Testing Filters start_end_callpattern')
        open_report(self.reports_view, 'Testing Filters start_end_callpattern')
        apply_filter(self.all_calls, start_time='2017-11-06 14:34', end_time='2017-11-06 14:35', n_patterns=1)
        verify_kpis(self.kpis_objects, start_end_callpattern_filter_dict)  # Bug Ticket ST-1062
        delete_report(self.reports_view, 'Testing Filters start_end_callpattern')

    #     # TODO: Missing data rethink this TC as per ST-945
    #
    # # TODO: do the same with filter_by_from_and_to_headers, filter_by_interface, filter_by_kpi_boundaries
    # # TODO: you'll have to follow the exact same steps and compare kpis for all tables
    # # TODO: to test for persistence too. This will yield errors in automation so, i'll add them later, when
    # # TODO: the current bugs are fixed or if I find another way to verify filters working, till then
    # # TODO: test manually using the following steps
    def test_4(self):  # TCST-514 : Testing Percentile
        login.login(self.driver, superuser, superuser_password)
        create_report(self.reports_view, self.create_reports_view,
                      [FIRST_CALL_PCAP, ERICSSON_ERICSSON_PCAP], False, 'Testing Filters percentile')
        open_report(self.reports_view, 'Testing Filters percentile')
        apply_filter(self.all_calls, percentile={'filter_percentile': '40'})
        verify_kpis(self.kpis_objects, non_anonymized_dict) # Bug Ticket ST-1062

        ''' Report -> MOS Feature -> Invalid Uploads '''

    def test_5(self):  # TCST-506 : Non-CSV File upload
        login.login(self.driver, adminuser, adminuser_password)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-506')
        open_report(self.reports_view, 'TCST-506')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_381_SH, delimiter=',',
                                                   expected_message='The uploaded file must be a CSV file.')
        delete_report(self.reports_view, 'TCST-506')

    def test_6(self):  # TCST-507 : MOS File missing obligatory header
        login.login(self.driver, adminuser, adminuser_password)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-507')
        open_report(self.reports_view, 'TCST-507')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_507_A_PARTYNUMBER_MISSING_CSV,
                                                   delimiter='\t',
                                                   expected_message='CSV file must contain all the mandatory headers.')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_507_B_PARTYNUMBER_MISSING_CSV,
                                                   delimiter='\t',
                                                   expected_message='CSV file must contain all the mandatory headers.')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_507_DIALINGTIME_CET_MISSING_CSV,
                                                   delimiter='\t',
                                                   expected_message='CSV file must contain all the mandatory headers.')
        delete_report(self.reports_view, 'TCST-507')

    ''' Reports -> MOS Feature -> Valid Uploads '''

    def test_7(self):  # TCST-505 : MOS correlation to "All Calls"
        login.login(self.driver, superuser, superuser_password)
        create_report(self.reports_view, self.create_reports_view, [MOS_CLABOR_PACP], False,
                      'TCST-505')
        open_report(self.reports_view, 'TCST-505')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_505, ';', True,
                                                   'MOS statistics CSV file has been uploaded successfully', True)
        self.driver.refresh()
        self.all_calls.open()
        self.all_calls.download_kpi_as_csv()
        self.all_calls.compare_csv(TCST_505_AC_VALUES)
        delete_report(self.reports_view, 'TCST-505')

    def test_8(self):  # TCST-509 : Multiple MOS Uploads
        login.login(self.driver, adminuser, adminuser_password)
        create_report(self.reports_view, self.create_reports_view, [MOS_CLABOR_PACP], False,
                      'TCST-509')
        open_report(self.reports_view, 'TCST-509')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_509_MOS_PART1,
                                                   expected_message='Calls in report could not be matched with the provided MOS file.')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_509_MOS_PART2,
                                                   expected_message='Calls in report could not be matched with the provided MOS file.')
        upload_download_mos_verify_message_and_kpi(self.all_calls, TCST_509_MOS_PART2, download_verify_kpi=True)
        delete_report(self.reports_view, 'TCST-509')

    def test_9(self):  # TCST-512 : User with all permissions - Report anonymized
        login.login(self.driver, adminuser, adminuser_password)
        create_report(self.reports_view, self.create_reports_view, [MOS_CLABOR_PACP], True,
                      'TCST-512')
        open_report(self.reports_view, 'TCST-512')
        # TODO: either delete verify_own_report if case is not needed or change it's signature to match new signature
        verify_own_report_actions(self.all_calls, 'TCST-512', True, delete=True)

    # TODO: add MOS TC where you upload a PCAP and MOS file and see correlated info in AllCalls. Data for that are
    # on the desktop under KPI analysis folder. Need to clarify something with Tariq first.
    # def test_62(self): # TCST-505 : INCOMPLETE User with all permissions - MOS correlation to "All Calls"


if __name__ == '__main__':
    unittest.main()
