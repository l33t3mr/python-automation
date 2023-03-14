import unittest

from Modules import login, logout
from Modules.authorization_info import url, superuser, superuser_password, adminuser, adminuser_password
from Modules.helpers import create_user, delete_user, create_report, open_report, \
    verify_all_report_actions_except_edit_delete_enabled, verify_only_download_pcaps_enabled_in_report_actions, \
    check_viewing_permissions_and_restrictions_on_report, verify_all_report_actions_disabled, \
    verify_only_edit_and_delete_enabled_in_report_actions, verify_all_report_actions_enabled
from Modules.shared_objects import create_reports_view, create_create_reports_view, create_users_view, \
    create_groups_view, create_kpi_objects, create_firefox_driver
from Data.data_path import FIRST_CALL_PCAP


class ShareReportAndReportOptions(unittest.TestCase):

    def setUp(self):
        self.driver = create_firefox_driver(url, __name__)
        login.login(self.driver, adminuser, adminuser_password)
        self.reports_view = create_reports_view(self.driver)
        self.create_reports_view = create_create_reports_view(self.driver)
        self.user_view = create_users_view(self.driver)
        self.group_view = create_groups_view(self.driver)
        self.kpis_objects = create_kpi_objects(self.driver)
        self.all_calls = create_kpi_objects(self.driver)['Report Level']['AllCalls']
        self.all_viewing_permissions = ['Can view SIP Call-ID',
                                        'Can view SIP From, To and the P-Asserted-Identity headers',
                                        'Can view UA types',
                                        'Can view IP addresses', 'Can view IMS node names']
        self.call_id_and_from_to_permissions = ['Can view SIP Call-ID',
                                                'Can view SIP From, To and the P-Asserted-Identity headers']
        self.no_viewing_permissions = []

    def tearDown(self):
        logout.logout(self.driver)
        self.driver.quit()

    def test_1(self):  # TCST-516 : Sharing a Report between normal users with all viewing permissions
        user1 = 'Test1_1'
        user2 = 'Test1_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.all_viewing_permissions)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test1_1', username=user2)
        open_report(self.reports_view, 'Created by Test1_1')
        verify_all_report_actions_enabled(self.all_calls)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test1_1')
        verify_all_report_actions_except_edit_delete_enabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user2)
        delete_user(self.user_view, user1)

    def test_2(self):  # TCST-518 : Sharing a Report between user with all viewing permissions and user without any
        user1 = 'Test2_1'
        user2 = 'Test2_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.no_viewing_permissions)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test2_1', username=user2)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test2_1')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user2)
        delete_user(self.user_view, user1)

    def test_3(self):  # TCST-519 : Sharing a Report between user with all viewing permissions and user with some
        user1 = 'Test3_1'
        user2 = 'Test3_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.call_id_and_from_to_permissions)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test3_1', username=user2)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test3_1')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_call_id=True,
                                                             can_view_sip_from_to_p_asserted=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user2)
        delete_user(self.user_view, user1)

    def test_4(self):  # TCST-520 : Admin can see all reports created regardless of report owner permissions
        user1 = 'Test4_1'
        user2 = 'Test4_2'
        user3 = 'Test4_3'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.call_id_and_from_to_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user3, password=user3 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test4_1')
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test4_2')
        logout.logout(self.driver)
        login.login(self.driver, user3, user3 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test4_3')
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        open_report(self.reports_view, 'Created by Test4_1')
        verify_all_report_actions_enabled(self.all_calls)
        open_report(self.reports_view, 'Created by Test4_2')
        verify_all_report_actions_enabled(self.all_calls)
        open_report(self.reports_view, 'Created by Test4_3')
        verify_all_report_actions_enabled(self.all_calls)
        delete_user(self.user_view, user3)
        delete_user(self.user_view, user2)
        delete_user(self.user_view, user1)

    def test_5(self):  # TCST-521 : Sharing a Report between an admin and a normal user with no viewing permissions
        user1 = 'Test5'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Admin_Test5', username=user1)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        open_report(self.reports_view, 'Created by Admin_Test5')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)


    def test_6(self):  # TCST-522 : Sharing a Report between an admin and a normal user with some viewing permissions
        user1 = 'Test6'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.call_id_and_from_to_permissions,
                    create_non_anonymized=True)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Admin_Test6', username=user1)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        open_report(self.reports_view, 'Created by Admin_Test6')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_call_id=True,
                                                             can_view_sip_from_to_p_asserted=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)

    def test_7(self):  # TCST-523 : Sharing a Report between an admin and a normal user with all viewing permissions
        user1 = 'Test7'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Admin_Test7', username=user1)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        open_report(self.reports_view, 'Created by Admin_Test7')
        verify_all_report_actions_except_edit_delete_enabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)

    def test_8(self):  # TCST-524 : Sharing a Report between user without viewing permissions and one with all permiss.
        user1 = 'Test8_1'
        user2 = 'Test8_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.all_viewing_permissions,
                    create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test8_1', username=user2)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test8_1')
        verify_all_report_actions_except_edit_delete_enabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)
        delete_user(self.user_view, user2)

    def test_9(self):  # TCST-525 : Sharing a Report between a user without  permissions and a user with some permiss.
        user1 = 'Test9_1'
        user2 = 'Test9_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.call_id_and_from_to_permissions,
                    create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test9_1', username=user2)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test9_1')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)
        delete_user(self.user_view, user2)

    def test_10(self):  # TCST-526 : Sharing a Report between user without permissions and a user without permiss.
        user1 = 'Test10_1'
        user2 = 'Test10_2'
        create_user(self.user_view, user1, password=user1 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        create_user(self.user_view, user2, password=user2 * 3, view_permissions=self.no_viewing_permissions,
                    create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, user1, user1 * 3)
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'Created by Test10_1', username=user2)
        logout.logout(self.driver)
        login.login(self.driver, user2, user2 * 3)
        open_report(self.reports_view, 'Created by Test10_1')
        verify_all_report_actions_disabled(self.all_calls)
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.user_view, user1)
        delete_user(self.user_view, user2)

    def test_11(self):  # TCST-537 : Report Options on Anonymized Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], True,
                      'Created by Admin_Test8')
        open_report(self.reports_view, 'Created by Admin_Test8')
        verify_only_edit_and_delete_enabled_in_report_actions(self.all_calls)


if __name__ == '__main__':
    unittest.main()
