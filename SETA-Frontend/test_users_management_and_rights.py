import unittest
import time

from Modules.helpers import *
from Modules.shared_objects import *
from Modules import login, logout
from Modules.authorization_info import superuser, superuser_password, adminuser, adminuser_password, url

from Data.data_path import FIRST_CALL_PCAP
from Data.OriginalConfigurations.OriginalConfigurationsData import original_ip_mapping_csv, \
    original_interface_configuration_csv

testuser_password = 'OnePassword2Rul3'


class UsersManagementAndRights(unittest.TestCase):

    def setUp(self):
        self.driver = create_firefox_driver(url, __name__)
        self.groups_view = create_groups_view(self.driver)
        self.users_view = create_users_view(self.driver)
        self.django_admin_view = create_django_admin_view(self.driver)
        self.my_profile_view = create_my_profile_view(self.driver)
        self.interface_config_view = create_interface_config_view(self.driver)
        self.ip_mappings_view = create_ip_mappings_view(self.driver)
        self.reports_view = create_reports_view(self.driver)
        self.create_reports_view = create_create_reports_view(self.driver)
        self.kpis_objects = create_kpi_objects(self.driver)

    def tearDown(self):
        logout.logout(self.driver)
        self.driver.quit()

        ''' User Managements and Rights -> Modify Users and Groups'''

    # TODO: add two testcases where admin and superuser change their own data

    def test_1(self):  # TCST-85 : Modify Self over User Profile (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-85-admin', group='admin', password=adminuser_password)
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-85-admin', adminuser_password)
        change_user_profile_data_then_undo_changes(self.my_profile_view, 'TCST-85-admin', adminuser_password, None,
                                                   None, None, 'Europe/Berlin', 'TCST-85-admin-new',
                                                   'TCST-85-FN@seta.com', 'TCST-85-FN', 'TCST-85-admin-LN',
                                                   'Europe/Belgrade')
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-85-admin')

    def test_2(self):  # TCST-83 : Modify Normal Group (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_group(self.groups_view, 'TCST-83', ['admin', 'user'], create_non_anonymized=False)
        modify_group(self.groups_view, 'TCST-83', 'TCST-83x', ['admin'], create_non_anonymized=True)
        delete_group(self.groups_view, 'TCST-83x')

    def test_3(self):  # TCST-82 : Delete Normal Group (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_group(self.groups_view, 'TCST-82', create_non_anonymized=False)
        delete_group(self.groups_view, 'TCST-82')

    def test_4(self):
        # TCST-81 : Delete normal User (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-81', password='TCST-81TCST-81')
        delete_user(self.users_view, 'TCST-81')

    def test_5(self):  # TCST-80 : Modify Normal User (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-80', password='TCST-80TCST-80')
        modify_user_over_users_section(self.users_view, 'TCST-80', 'TCST-80x', 'TCST-80xTCST-80x', 'NA@na.com', 'Test',
                                       'Testx', None,
                                       None, 'Europe/Belgrade')
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-80x')

    def test_6(self):  # TCST-79 : Modify Admin User (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-79-admin', group='admin', password=adminuser_password)
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-79-admin', adminuser_password)
        modify_user_over_users_section(self.users_view, 'TCST-79-admin', 'TCST-79-admin-new', 'TCST-79xTCST-79x',
                                       'admin@admin.com',
                                       'admin',
                                       'adminx', None, None, 'Europe/Belgrade')
        modify_user_over_users_section(self.users_view, 'TCST-79-admin-new', 'TCST-79-admin', adminuser_password,
                                       'admin@seta.com', 'Mr.',
                                       'Admin', None, None, 'Europe/Berlin')
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-79-admin')

    def test_7(self):  # TCST-78 : Modify Admin Group (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        self.groups_view.open()
        self.groups_view.find_group_modify_via_operations('admin')
        self.groups_view.verify_group_name_disabled_and_hint()

    def test_8(self):  # TCST-77 : Delete Admin Group (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        self.groups_view.open()
        self.groups_view.verify_can_not_delete_admin_group()

    def test_9(self):  # TCST-76 : Delete Admin User (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-76', None, None, None, 'admin', 'TCST-76xTCST-76x')
        delete_user(self.users_view, 'TCST-76')

    def test_10(self):  # TCST-74 : Delete Admin User (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-74', group='admin', password='TCST-74xTCST-74x')
        delete_user(self.users_view, 'TCST-74')

    def test_11(self):  # TCST-73 : Delete Admin Group (Superuser)
        login.login(self.driver, superuser, superuser_password)
        self.groups_view.open()
        self.groups_view.find_group_delete_via_operations('admin')
        self.groups_view.verify_can_not_delete_admin_group()

    def test_12(self):  # TCST-72 : Modify Admin Group (Superuser)
        login.login(self.driver, superuser, superuser_password)
        self.groups_view.open()
        self.groups_view.find_group_modify_via_operations('admin')
        self.groups_view.verify_group_name_disabled_and_hint()

    def test_13(self):  # TCST-70 : Modify Superuser (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        users = Users.Users(self.driver)
        users.open()
        users.find_and_modify_user_via_edit_operation('user')
        users.verify_user_cannot_edit_other_users_profiles('user')
        users.verify_user_cannot_delete_other_users_profiles('user')

    def test_14(self):  # TCST-69 : Modify Admin User (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-69-Admin', group='admin', password=adminuser_password)
        modify_user_over_users_section(self.users_view, 'TCST-69-Admin', 'TCST-69-new-admin', 'TCST-69xTCST-69x',
                                       'admin@admin.com',
                                       'admin',
                                       'adminx', None, None, 'Europe/Belgrade')
        modify_user_over_users_section(self.users_view, 'TCST-69-new-admin', 'TCST-69-Admin', adminuser_password,
                                       'admin@seta.com', 'Mr.',
                                       'Admin', None,
                                       None,
                                       'Europe/Berlin')
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-69-Admin')

    def test_15(self):  # TCST-67 : Delete Normal Group (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_group(self.groups_view, 'TCST-67', create_non_anonymized=False)
        delete_group(self.groups_view, 'TCST-67')

    def test_16(self):  # TCST-71 : Modify Normal Group (Superuser)
        login.login(self.driver, adminuser, adminuser_password)
        create_group(self.groups_view, 'TCST-71', ['admin', 'user'], None, False)
        modify_group(self.groups_view, 'TCST-71', 'TCST-71x', ['admin'], None, True)
        delete_group(self.groups_view, 'TCST-71x')

    def test_17(self):  # TCST-84 : Modify Self over User Profile (User)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-84', password='TCST-84xTCST-84x')
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-84', 'TCST-84xTCST-84x')
        change_user_profile_data_then_undo_changes(self.my_profile_view, 'TCST-84', 'TCST-84xTCST-84x', None, None,
                                                   None,
                                                   None,
                                                   'TCST-84-new', 'TCST-84@seta.com', 'Test', 'UserX',
                                                   'Europe/Belgrade')
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-84')

    '''Users Management and Rights -> Ip Mapping'''

    def test_18(self):  # TCST-44 : IP Mapping Changes(changing User to Admin and vice versa)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-44', group='admin', password='TCST-44TCST-44')
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-44', 'TCST-44TCST-44')
        verify_message_after_adding_entries(self.ip_mappings_view,
                                            [('x', 'y', '10.10.10.10'), ('c', 's', '20.20.20.20')])
        verify_mapping_upload_succeeded(self.ip_mappings_view, original_ip_mapping_csv)
        self.users_view.open()
        self.users_view.wait_mapping_load()
        self.users_view.find_and_modify_user_via_edit_operation('TCST-44')
        self.users_view.clear_groups_field_in_user_form()
        self.users_view.verify_message('Successfully updated user "TCST-44"')
        self.ip_mappings_view.open()
        assert not self.ip_mappings_view.is_add_entries_to_mapping_enabled()
        assert not self.ip_mappings_view.is_upload_mappings_enabled()
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-44')

    '''Users Management and Rights -> Interface Config'''

    def test_19(self):  # TCST-48 : Interface Config Changes(changing User to Admin and vice versa)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-48', group='admin', password='TCST-48TCST-48')
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-48', 'TCST-48TCST-48')
        verify_message_after_adding_entries(self.interface_config_view,
                                            [('xxx', 'yyy', 'zzz', 'both'), ('aaa', 'bbb', 'ccc', 'both')])
        verify_mapping_upload_succeeded(self.interface_config_view, original_interface_configuration_csv)
        self.users_view.open()
        self.users_view.wait_mapping_load()
        self.users_view.find_and_modify_user_via_edit_operation('TCST-48')
        self.users_view.clear_groups_field_in_user_form()
        self.users_view.verify_message('Successfully updated user "TCST-48"')
        self.interface_config_view.open()
        assert not self.interface_config_view.is_add_entries_to_mapping_enabled()
        assert not self.interface_config_view.is_upload_mappings_enabled()
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-48')

    '''Users Management and Rights -> Anonymization in Users & Groups -> Users'''

    def test_20(self):  # TCST-104 : Admin can create non-anonymised reports(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)

    def test_21(self):  # TCST-101 : User can't create non-anonymised reports(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-101', password='TCST-101TCST-101',
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'], create_non_anonymized=False)
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-101', 'TCST-101TCST-101')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, False)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-101')

    def test_22(self):  # TCST-425 User can create non-anonymised reports(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-425', password='TCST-425TCST-425',
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'], create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-425', 'TCST-425TCST-425')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-425')

    def test_23(self):  # TCST-91 : User anonymization changing(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # create user without permission to non-anonymize
        create_user(self.users_view, 'TCST-91', password='TCST-91TCST-91', create_non_anonymized=False)
        # login with the new user and test if anonymize
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-91', 'TCST-91TCST-91')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, False)
        # change user and allow him to non-anonymize
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        modify_user_over_users_section(self.users_view, 'TCST-91', 'TCST-91', new_password=None,
                                       create_non_anonymized=True)
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        # Clean up, delete groups and user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-91')

    '''Users Management and Rights -> Anonymization in Users & Groups -> Groups'''

    def test_24(self):  # TCST-98 : Group can't create non-anonymised reports(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-98', password='TCST-98TCST-98', create_non_anonymized=False)
        create_group(self.groups_view, 'must anonymize TCST-98', ['TCST-98'], None, False)
        logout.logout(self.driver)
        # login with the new user and test if can anonymize
        login.login(self.driver, 'TCST-98', 'TCST-98TCST-98')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, False)
        # Clean up, delete groups and user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-98')
        delete_group(self.groups_view, 'must anonymize TCST-98')

    def test_25(self):  # TCST-96 : Group can create non-anonymised reports(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-96', password='TCST-96TCST-96', create_non_anonymized=False)
        create_group(self.groups_view, 'can non-anonymize TCST-96', ['TCST-96'],
                     ['Can view SIP Call-ID', 'Can view SIP From, To and the P-Asserted-Identity headers',
                      'Can view UA types',
                      'Can view IP addresses', 'Can view IMS node names'], True)
        # login with the new user and test if can not-anonymize
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-96', 'TCST-96TCST-96')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        # Clean up, delete groups and user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-96')
        delete_group(self.groups_view, 'can non-anonymize TCST-96')

    def test_26(self):  # TCST-56 : User in 2 different anonymization right groups(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-56', password='TCST-56TCST-56', create_non_anonymized=False)
        create_group(self.groups_view, 'Can non-anonymize TCST-56', ['TCST-56'], None, True)
        create_group(self.groups_view, 'must anonymize TCST-56', ['TCST-56'], None, False)
        logout.logout(self.driver)
        # login with the new user and test if can anonymize
        login.login(self.driver, 'TCST-56', 'TCST-56TCST-56')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        # Clean up, delete groups and user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_group(self.groups_view, 'Can non-anonymize TCST-56')
        delete_group(self.groups_view, 'must anonymize TCST-56')
        delete_user(self.users_view, 'TCST-56')

    '''Users Management and Rights -> Anonymization in Users & Groups -> Mix Users & Groups'''

    def test_27(self):  # TCST-90 : User can't create non-anonymised, group can(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # create user without permission to non-anonymize
        create_user(self.users_view, 'TCST-90', password='TCST-90TCST-90', create_non_anonymized=False)
        # create group with permission and add user to it
        create_group(self.groups_view, 'can non-anonymize TCST-90', ['TCST-90'],
                     viewing_permissions=['Can view SIP Call-ID',
                                          'Can view SIP From, To and the P-Asserted-Identity headers',
                                          'Can view UA types',
                                          'Can view IP addresses', 'Can view IMS node names'],
                     create_non_anonymized=True)
        # test if user can create non-anonymized reports
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-90', 'TCST-90TCST-90')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        # clean up
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-90')
        delete_group(self.groups_view, 'can non-anonymize TCST-90')

    def test_28(self):  # TCST-92 : User can create non-anonymised, group can't(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # create user with permission to non-anonymize
        create_user(self.users_view, 'TCST-92', password='TCST-92TCST-92',
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'], create_non_anonymized=True)
        # create group without permission to non-anonymize
        create_group(self.groups_view, 'must anonymize TCST-92', ['TCST-92'], None, False)
        # login with the new user and test if can not-anonymize
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-92', 'TCST-92TCST-92')
        verify_user_can_create_non_anonymized_reports(self.reports_view, self.create_reports_view, True)
        # Clean up, delete groups and user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-92')
        delete_group(self.groups_view, 'must anonymize TCST-92')

    '''Users Management and Rights -> Creating Users & Groups:
    Most of the TCSTS here are covered in previous TCSTS. Only the not covered are here.'''

    def test_29(self):  # TCST-63 : Group Creation (normal User)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-63', password='TCST-63TCST-63')
        # login with the new user and check Groups option not visible in settings
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-63', 'TCST-63TCST-63')
        groups = Groups.Groups(self.driver)
        groups.groups_tab_invisible()
        # logout and clean up
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-63')

    def test_30(self):  # TCST-61 : User Creation (normal User)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-61', password='TCST-61TCST-61')
        # login with the new user and check Users option not visibile in settings
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-61', 'TCST-61TCST-61')
        users = Users.Users(self.driver)
        users.verify_user_cannot_see_users_tab()
        # logout and clean up
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-61')

    '''Users Management and Rights -> DTAG Password Policy'''

    def test_31(self):  # TCST-246 : Entering wrong password 5x blocks the user for 24H (Admin)
        login.login(self.driver, superuser, superuser_password)
        verify_user_blocked_when_logging_in_with_wrong_password(self.users_view, self.django_admin_view, 'TCST-246',
                                                                testuser_password, True)

    def test_32(self):  # TCST-245 : Entering wrong password 5x blocks the user for 24H (Superuser)
        login.login(self.driver, superuser, superuser_password)
        verify_user_blocked_when_logging_in_with_wrong_password(self.users_view, self.django_admin_view, 'TCST-245',
                                                                testuser_password,
                                                                user_type_superuser=True)

    def test_33(self):  # TCST-244 : Entering wrong password 5x blocks the user for 24H (Normal User)
        login.login(self.driver, superuser, superuser_password)
        verify_user_blocked_when_logging_in_with_wrong_password(self.users_view, self.django_admin_view, 'TCST-244',
                                                                testuser_password)

    def test_34(self):  # TCST-243 : Changing own password (Superuser)
        login.login(self.driver, superuser, superuser_password)
        verify_dtag_password_policy_adhered(self.users_view, self.django_admin_view, self.my_profile_view, 'TCST-243',
                                            testuser_password, user_type_superuser=True)

    def test_35(self):  # TCST-242 : Changing own password (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        verify_dtag_password_policy_adhered(self.users_view, self.django_admin_view, self.my_profile_view,
                                            'TCST-242', testuser_password, True)

    def test_36(self):  # TCST-241 : Changing own password (Normal User)
        # precondition: create a normal user
        login.login(self.driver, superuser, superuser_password)
        verify_dtag_password_policy_adhered(self.users_view, self.django_admin_view, self.my_profile_view,
                                            'TCST-241', testuser_password)

    ''' Users Management and Rights -> Viewing Permissions in Users & Groups '''

    def test_37(self):  # TCST-392: User has permission to view only one column(Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-392', password='TCST-392TCST-392', view_permissions=['Can view SIP Call-ID'],
                    create_non_anonymized=True)
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-392', 'TCST-392TCST-392')
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-392_callid')
        open_report(self.reports_view, 'TCST-392_callid')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_call_id=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-392')

    def test_38(self):  # TCST-393 : User has no permission to view (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User  and assign no permissions
        create_user(self.users_view, 'TCST-393', password='TCST-393TCST-393', create_non_anonymized=True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-393', 'TCST-393TCST-393')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-393_nopermisions')
        open_report(self.reports_view, 'TCST-393_nopermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-393')

    def test_39(self):  # TCST-394 : User has all permissions (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User  and assign all permission
        create_user(self.users_view, 'TCST-394', password='TCST-394TCST-394', create_non_anonymized=True,
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-394', 'TCST-394TCST-394')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-394_allpermisions')
        open_report(self.reports_view, 'TCST-394_allpermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-394')

    def test_40(self):  # TCST-395 : User has more than one permission (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-395', password='TCST-395TCST-395', create_non_anonymized=True,
                    view_permissions=['Can view SIP From, To and the P-Asserted-Identity headers',
                                      'Can view IP addresses',
                                      'Can view IMS node names'])
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-395', 'TCST-395TCST-395')
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-395_multiplepermisions')
        open_report(self.reports_view, 'TCST-395_multiplepermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_ims_node_names=True,
                                                             can_view_ip_address=True,
                                                             can_view_sip_from_to_p_asserted=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-395')

    def test_41(self):  # TCST-419 : Admin User has all permissions
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User  and assign all permissions
        create_user(self.users_view, 'TCST-419', password='TCST-419TCST-419', create_non_anonymized=True,
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-419', 'TCST-419TCST-419')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-419_allpermisions')
        open_report(self.reports_view, 'TCST-419_allpermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-419')

    def test_42(self, ):  # TCST-403 : User has permission to view only one column (Superuser)
        login.login(self.driver, superuser, superuser_password)
        # Precondition Create User  and assign permission 'Call ID'
        create_user(self.users_view, 'TCST-403', password='TCST-403TCST-403', create_non_anonymized=True,
                    view_permissions=['Can view SIP Call-ID'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-403', 'TCST-403TCST-403')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-403_callid')
        open_report(self.reports_view, 'TCST-403_callid')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_call_id=True)
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-403')

    def test_43(self):  # TCST-404 : User has no permission to view (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-404', password='TCST-404TCST-404', create_non_anonymized=True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-404', 'TCST-404TCST-404')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-404_nopermisions')
        open_report(self.reports_view, 'TCST-404_nopermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-404')

    def test_44(self):  # TCST-406 : User has all permissions (Superuser)
        login.login(self.driver, superuser, superuser_password)
        # Precondition Create User  and assign all permissions
        create_user(self.users_view, 'TCST-406', password='TCST-406TCST-406', create_non_anonymized=True,
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-406', 'TCST-406TCST-406')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-406_allpermisions')
        open_report(self.reports_view, 'TCST-406_allpermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-406')

    def test_45(self):  # TCST-407 : User has more than one permission (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-407', password='TCST-407TCST-407', create_non_anonymized=True,
                    view_permissions=['Can view SIP From, To and the P-Asserted-Identity headers',
                                      'Can view IP addresses',
                                      'Can view IMS node names'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-407', 'TCST-407TCST-407')
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-407_multiplepermisions')
        open_report(self.reports_view, 'TCST-407_multiplepermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_from_to_p_asserted=True,
                                                             can_view_ims_node_names=True, can_view_ip_address=True)
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-407')

    def test_46(self):  # TCST-420 : Superuser has all permissions
        login.login(self.driver, superuser, superuser_password)
        # Precondition Create User  and assign all permissions
        create_user(self.users_view, 'TCST-420', password='TCST-420TCST-420', create_non_anonymized=True,
                    view_permissions=['Can view SIP Call-ID',
                                      'Can view SIP From, To and the P-Asserted-Identity headers', 'Can view UA types',
                                      'Can view IP addresses', 'Can view IMS node names'])
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-420', 'TCST-420TCST-420')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-420_allpermisions')
        open_report(self.reports_view, 'TCST-420_allpermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-420')

    '''Users Management and Rights -> Viewing permissions in Users & Groups -> Groups'''

    def test_47(self):  # TCST-411 : Group has more than one permission
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User
        create_user(self.users_view, 'TCST-411', password='TCST-411TCST-411')
        create_group(self.groups_view, 'TCST-411', ['TCST-411'],
                     viewing_permissions=['Can view SIP From, To and the P-Asserted-Identity headers',
                                          'Can view IP addresses',
                                          'Can view IMS node names'], create_non_anonymized=True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-411', 'TCST-411TCST-411')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-411_multiplepermisions')
        open_report(self.reports_view, 'TCST-411_multiplepermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_from_to_p_asserted=True,
                                                             can_view_ims_node_names=True, can_view_ip_address=True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-411')
        delete_group(self.groups_view, 'TCST-411')

    def test_48(self):  # TCST-410 : Group has all permissions
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User
        create_user(self.users_view, 'TCST-410', password='TCST-410TCST-410')
        # Precondition Create group and add user to it, assign all permissions
        create_group(self.groups_view, 'TCST-410', ['TCST-410'],
                     ['Can view SIP Call-ID', 'Can view SIP From, To and the P-Asserted-Identity headers',
                      'Can view UA types',
                      'Can view IP addresses', 'Can view IMS node names'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-410', 'TCST-410TCST-410')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-410_allpermisions')
        open_report(self.reports_view, 'TCST-410_allpermisions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-410')
        delete_group(self.groups_view, 'TCST-410')

    def test_49(self):  # TCST-409 : Group has no permission to view (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-409', password='TCST-409TCST-409')
        # Precondition Create group and add user to it, assign no permissions
        create_group(self.groups_view, 'TCST-409', ['TCST-409'], create_non_anonymized=True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-409', 'TCST-409TCST-409')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-409_nopermissions')
        open_report(self.reports_view, 'TCST-409_nopermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-409')
        delete_group(self.groups_view, 'TCST-409')

    def test_50(self):  # TCST-408 : Group has permission to view only one column (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        create_user(self.users_view, 'TCST-408', password='TCST-408TCST-408')
        create_group(self.groups_view, 'TCST-408', ['TCST-408'], ['Can view SIP Call-ID'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-408', 'TCST-408TCST-408')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-408_callid')
        open_report(self.reports_view, 'TCST-408_callid')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects,
                                                             can_view_sip_call_id=True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-408')
        delete_group(self.groups_view, 'TCST-408')

    def test_51(self):  # TCST-415 : Group has more than one permission (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-415', password='TCST-415TCST-415')
        create_group(self.groups_view, 'TCST-415', ['TCST-415'],
                     ['Can view SIP From, To and the P-Asserted-Identity headers', 'Can view IP addresses',
                      'Can view IMS node names'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-415', 'TCST-415TCST-415')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-415_multipermissions')
        open_report(self.reports_view, 'TCST-415_multipermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_from_to_p_asserted=True,
                                                             can_view_ip_address=True, can_view_ims_node_names=True)
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-415')
        delete_group(self.groups_view, 'TCST-415')

    def test_52(self):  # TCST-414 : Group has all permissions (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-414', password='TCST-414TCST-414')
        create_group(self.groups_view, 'TCST-414', ['TCST-414'],
                     ['Can view SIP Call-ID', 'Can view SIP From, To and the P-Asserted-Identity headers',
                      'Can view UA types',
                      'Can view IP addresses', 'Can view IMS node names'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-414', 'TCST-414TCST-414')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-414_allpermissions')
        open_report(self.reports_view, 'TCST-414_allpermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-414')
        delete_group(self.groups_view, 'TCST-414')

    def test_53(self):  # TCST-413 : Group has no permission to view (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-413', password='TCST-413TCST-413')
        create_group(self.groups_view, 'TCST-413', ['TCST-413'], None, True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-413', 'TCST-413TCST-413')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-413_nopermissions')
        open_report(self.reports_view, 'TCST-413_nopermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-413')
        delete_group(self.groups_view, 'TCST-413')

    def test_54(self):  # TCST-412 : Group has permission to view only one column (Superuser)
        login.login(self.driver, superuser, superuser_password)
        create_user(self.users_view, 'TCST-412', password='TCST-412TCST-412')
        create_group(self.groups_view, 'TCST-412', ['TCST-412'], ['Can view SIP Call-ID'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-412', 'TCST-412TCST-412')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-412_callid')
        open_report(self.reports_view, 'TCST-412_callid')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_call_id=True)
        logout.logout(self.driver)
        login.login(self.driver, superuser, superuser_password)
        delete_user(self.users_view, 'TCST-412')
        delete_group(self.groups_view, 'TCST-412')

    '''Users Management and Rights -> Viewing permissions in Users & Groups -> Mix Users & Groups'''

    def test_55(self):  # TCST-416 : User with no permission, Group with more than one permission (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User
        create_user(self.users_view, 'TCST-416', password='TCST-416TCST-416',
                    view_permissions=['Can view SIP From, To and the P-Asserted-Identity headers',
                                      'Can view IP addresses',
                                      'Can view IMS node names'])
        create_group(self.groups_view, 'TCST-416', ['TCST-416'], ['Can view UA types', 'Can view SIP Call-ID'], True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-416', 'TCST-416TCST-416')
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-416_allpermissions')
        open_report(self.reports_view, 'TCST-416_allpermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, True, True, True, True, True)
        # Clean up - delete user
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-416')
        delete_group(self.groups_view, 'TCST-416')

    def test_56(self):  # TCST-417 : Group with no permission, User with more than one permission (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User
        create_user(self.users_view, 'TCST-417', password='TCST-417TCST-417',
                    view_permissions=['Can view SIP From, To and the P-Asserted-Identity headers',
                                      'Can view IP addresses',
                                      'Can view IMS node names'])
        create_group(self.groups_view, 'TCST-417', ['TCST-417'], create_non_anonymized=True)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-417', 'TCST-417TCST-417')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-417_multiplepermissions')
        open_report(self.reports_view, 'TCST-417_multiplepermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_from_to_p_asserted=True,
                                                             can_view_ip_address=True, can_view_ims_node_names=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-417')
        delete_group(self.groups_view, 'TCST-417')

    def test_57(self):  # TCST-418 : User with 2 Groups, one with, the other without (Admin)
        login.login(self.driver, adminuser, adminuser_password)
        # Precondition Create User
        create_user(self.users_view, 'TCST-418', password='TCST-418TCST-418')
        create_group(self.groups_view, 'TCST-418_all_viewing_permissions', ['TCST-418'],
                     ['Can view SIP From, To and the P-Asserted-Identity headers', 'Can view IP addresses',
                      'Can view IMS node names'], True)

        create_group(self.groups_view, 'TCST-418_no_viewing_permissions', ['TCST-418'], None, False)
        # Login with the new user
        logout.logout(self.driver)
        login.login(self.driver, 'TCST-418', 'TCST-418TCST-418')
        # Create Report
        create_report(self.reports_view, self.create_reports_view, [FIRST_CALL_PCAP], False,
                      'TCST-418_multiplepermissions')
        open_report(self.reports_view, 'TCST-418_multiplepermissions')
        check_viewing_permissions_and_restrictions_on_report(self.kpis_objects, can_view_sip_from_to_p_asserted=True,
                                                             can_view_ip_address=True,
                                                             can_view_ims_node_names=True)
        logout.logout(self.driver)
        login.login(self.driver, adminuser, adminuser_password)
        delete_user(self.users_view, 'TCST-418')
        delete_group(self.groups_view, 'TCST-418_all_viewing_permissions')
        delete_group(self.groups_view, 'TCST-418_no_viewing_permissions')


if __name__ == '__main__':
    unittest.main()
