import os

from Modules import login, logout
from Modules.authorization_info import superuser, superuser_password, adminuser, adminuser_password


# import threading
# lock = threading.Lock()


def verify_mapping_upload_succeeded(mapping_object, csv_file, csv_delimiter=',', csv_header_enabled=True):
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    mapping_last_upload_time = mapping_object.get_status()["active version"]
    mapping_object.upload_mapping(csv_file, csv_header_enabled, csv_delimiter)
    mapping_object.wait_status_color_stabilizes()
    assert not mapping_last_upload_time == mapping_object.get_status()[
        'active version'], 'Upload did not succeed. Active version before upload is {}'.format(mapping_last_upload_time)
    assert mapping_object.get_status()['status label'] == 'OK'


def verify_mapping_upload_fails(mapping_object, csv_file, csv_delimiter=',', expected_fail_message='No Message Entered',
                                csv_header_enabled=True):
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    mapping_last_upload_time = mapping_object.get_status()["active version"]
    mapping_object.upload_mapping(csv_file, csv_header_enabled, csv_delimiter)
    mapping_object.wait_status_color_stabilizes()
    if expected_fail_message == 'file must be csv':
        mapping_object.verify_message_file_must_be_csv()
    else:
        mapping_object.verify_message_upload_csv(expected_fail_message)
        assert mapping_last_upload_time == mapping_object.get_status()[
            "active version"], 'Upload did not fail. Active version before and after upload is {}'.format(
            mapping_last_upload_time)
        assert mapping_object.get_status()[
                   'status label'] == 'Error in latest upload. Mapping has not been updated.', ('Although Upload should'
                                                                                                ' have failed, status '
                                                                                                'label shows ok!')
        mapping_object.clear_failed_uploads_or_cancel_pending_uploads()


def verify_cancel_upload_button_works(mapping_object, csv_file, csv_delimiter=',', csv_header_enabled=True):
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    mapping_last_upload_time = mapping_object.get_status()["active version"]
    mapping_object.upload_mapping(csv_file, csv_header_enabled, csv_delimiter)
    mapping_object.clear_failed_uploads_or_cancel_pending_uploads()
    assert mapping_last_upload_time == mapping_object.get_status()[
        "active version"], 'Clear Pending Progress Button did not cancel upload'


def verify_clear_failed_upload_button_works(mapping_object, csv_file, csv_delimiter=',', csv_header_enabled=True):
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    mapping_last_upload_time = mapping_object.get_status()["active version"]
    mapping_object.upload_mapping(csv_file, csv_header_enabled, csv_delimiter)
    mapping_object.clear_failed_uploads_or_cancel_pending_uploads()
    assert mapping_last_upload_time == mapping_object.get_status()[
        "active version"], 'Clear Pending Progress Button did not cancel upload'


def verify_message_after_adding_entries(mapping_object, entries_to_add,
                                        message_to_verify='The data has been successfully added to the database.'):
    """
    Add entries to the Mapping Object and verify the content of the message that appears afterwards.

    :param mapping_object an object of either Interfaceconfig or IpMappings Class.
    :param entries_to_add: (list) of tuples each tuple has the following structure:
    1- Interface Config Tuple (first_node, second_node,interface,direction)
    2- Ip Mapping Tuple (node_name, ims_entity, ip_address)
    :param message_to_verify: the message content to verify
    """
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    mapping_object.wait_status_color_stabilizes()
    mapping_object.add_entries(entries_to_add)
    mapping_object.verify_message_add_entry(message_to_verify)


def verify_entries_get_deleted_successfully(mapping_object, entries_to_delete, bulk_delete=False):
    """
    Takes entries that are already saved/exist in the Mapping Object and delete them, either by bulk or single delete.

    :param mapping_object an object of either Interfaceconfig or IpMappings Class.
    :param entries_to_delete: (list) of tuples each tuple has the following structure:
    1- Interface Config Tuple (first_node, second_node,interface,direction)
    2- Ip Mapping Tuple (node_name, ims_entity, ip_address)
    :param bulk_delete if true, will delete the entries by selecting them first and clicking "Delete" button. Otherwise
    each element will be deleted by clicking on the "trash icon" next to it.
    """
    mapping_object.open()
    mapping_object.wait_for_add_entry_table_to_load()
    if bulk_delete:
        mapping_object.bulk_delete(entries_to_delete)
        mapping_object.verify_deleted(entries_to_delete)
    else:
        mapping_object.delete_entries(entries_to_delete)
        mapping_object.verify_deleted(entries_to_delete)


def verify_all_report_actions_enabled(kpi_object, mos_file_was_uploaded=False):
    """
    This functions is used to verify that download pcaps ,upload mos, edit and delete
    are enabled  in case the logged user is the owner with full viewing permissions and report
    is non-anonymized
    :param kpi_object: any object inheriting from KPIsReportLevel class
    :param mos_file_was_uploaded: if True, the "Download MOS CSV File" should be enabled
    otherwise disabled.
    """
    kpi_object.open()
    kpi_object.verify_download_merged_pcap_enabed_and_download_works()
    kpi_object.verify_download_original_pcaps_enabed_and_download_works()
    kpi_object.verify_mos_file_upload_enabled()
    if mos_file_was_uploaded:
        kpi_object.verify_mos_file_download_enabled()
    kpi_object.verify_mos_file_download_disabled()
    kpi_object.verify_edit_report_enabled()
    kpi_object.verify_delete_report_enabled()

def verify_all_report_actions_except_edit_delete_enabled(kpi_object, mos_file_was_uploaded=False):
    """
    This functions is used to verify that download pcaps and upload mos
    are enabled  and edit and delete are disabled in the case that a report
    is non-anonymized and owned by a user with full viewing permissions
    :param kpi_object: any object inheriting from KPIsReportLevel class
    :param mos_file_was_uploaded: if True, the "Download MOS CSV File" should be enabled
    otherwise disabled.
    """
    kpi_object.open()
    kpi_object.verify_download_merged_pcap_enabed_and_download_works()
    kpi_object.verify_download_original_pcaps_enabed_and_download_works()
    kpi_object.verify_mos_file_upload_enabled()
    if mos_file_was_uploaded:
        kpi_object.verify_mos_file_download_enabled()
    kpi_object.verify_mos_file_download_disabled()
    kpi_object.verify_edit_report_disabled()
    kpi_object.verify_delete_report_disabled()


# Shared in own->no perm // anony.own full permission and no permiss.
def verify_only_edit_and_delete_enabled_in_report_actions(kpi_object):
    """
    This function is used to verify that only Edit Report and Delete Report are enabled
    in Report actions when:
    1- User with no/missing permissions create a non-anonymized report
    2- User with no/missing permissions create an anonymized report
    3- User with all permissions create an anonymized report
    :param kpi_object: any object inheriting from KPIsReportLevel class
    """
    kpi_object.open()
    kpi_object.verify_download_merged_pcaps_disabled()
    kpi_object.verify_download_original_pcap_disabled()
    kpi_object.verify_mos_file_upload_disabled()
    kpi_object.verify_mos_file_download_disabled()
    kpi_object.verify_edit_report_enabled()
    kpi_object.verify_delete_report_enabled()


def verify_only_download_pcaps_enabled_in_report_actions(kpi_object):
    """
    This function is used to verify that only Download merged PCAP and Download
    original PCAPS are enabled in Report actions when:
    1- User with all permissions viewing shared non-anonymized report
    :param kpi_object: any object inheriting from KPIsReportLevel class
    """
    kpi_object.open()
    kpi_object.verify_download_original_pcaps_enabed_and_download_works()
    kpi_object.verify_download_original_pcaps_enabed_and_download_works()
    kpi_object.verify_mos_file_upload_disabled()
    kpi_object.verify_mos_file_download_disabled()
    kpi_object.verify_edit_report_disabled()
    kpi_object.verify_delete_report_disabled()


def verify_all_report_actions_disabled(kpi_object):
    """
    This function is used to verify that all Report actions are disabled when:
    1- User with no/missing permissions viewing shared non-anonymized report
    2- User with no/missing permissions viewing shared anonymized report
    3- User with full permissions viewing shared anonymized report
    :param kpi_object: any object inheriting from KPIsReportLevel class
    """
    kpi_object.open()
    kpi_object.verify_download_merged_pcaps_disabled()
    kpi_object.verify_download_original_pcap_disabled()
    kpi_object.verify_mos_file_upload_disabled()
    kpi_object.verify_mos_file_download_disabled()
    kpi_object.verify_edit_report_disabled()
    kpi_object.verify_delete_report_disabled()


"""
Non-Anony.:
1- Own Report -> All Enabled (All Viewing Permissions)  CHECKED
              -> Edit and Delete enabled (No Viewing Permissions) is this right? shouldn't an owner have access to download always? CHECKED 
2- Shared -> Only Download, no MOS (All Viewing Permissions) CHECK
          -> Nothing at all (No Viewing Permissions) CHECK


Anony.:
1- Own Report -> Edit and Delete enabled (All Viewing Permissions)
              -> Edit and Delete enabled (No Viewing Permissions)
2- Shared -> Nothing CHECKED

"""


def change_user_profile_data_then_undo_changes(my_profile_view, username, password, email, firstname,
                                               secondname, timezone, new_username, new_email,
                                               new_firstname, new_secondname, new_timezone):
    driver = my_profile_view.get_driver()
    my_profile_view.open()
    my_profile_view.wait_profile_loads()
    my_profile_view.verify_group_not_editable()
    my_profile_view.modify_my_profile(new_username, new_email, new_firstname, new_secondname, new_timezone)
    my_profile_view.verify_message('Successfully updated your profile')
    group_data = my_profile_view.get_my_profile_data()['groups']
    my_profile_should_be_data = [new_username, new_email, new_firstname, new_secondname, group_data, new_timezone]
    logout.logout(driver)
    login.login(driver, new_username, password)
    my_profile_view.open()
    my_profile_current_data = [value for value in my_profile_view.get_my_profile_data().values()]
    assert my_profile_current_data == my_profile_should_be_data, (
        'Profile data not changed! Current data: {}, should be data{}'.format(my_profile_current_data,
                                                                              my_profile_should_be_data))
    my_profile_view.modify_my_profile(username, email, firstname, secondname, timezone)


def create_group(groups_view, group_name, group_members_list=None, viewing_permissions=None,
                 create_non_anonymized=None):
    groups_view.open()
    groups_view.wait_mapping_load()
    groups_view.create_group(group_name, group_members_list, viewing_permissions, create_non_anonymized)
    groups_view.wait_mapping_load()
    groups_view.verify_message('Successfully created group "{}"'.format(group_name))


def modify_group(groups_view, old_group_name, new_group_name, new_group_members_list, viewing_permissions=None,
                 create_non_anonymized=None):
    groups_view.open()
    groups_view.wait_mapping_load()
    groups_view.find_group_modify_via_operations(old_group_name)
    groups_view.modify_group(new_group_name, new_group_members_list, viewing_permissions, create_non_anonymized)
    groups_view.wait_mapping_load()
    groups_view.verify_message('Successfully updated group "{}"'.format(new_group_name))


def delete_group(groups_view, group_name):
    groups_view.open()
    groups_view.wait_mapping_load()
    groups_view.find_group_delete_via_operations(group_name)
    groups_view.verify_delete_confirmation_content(group_name)
    groups_view.confirm_group_delete()
    groups_view.verify_message('Successfully deleted group')
    groups_view.verify_group_deleted(group_name)


def create_user(users_view, user_name, email=None, first_name=None, last_name=None, group=None, password=None,
                view_permissions=None, timezone=None, csv_header='check', csv_delimiter=',',
                create_non_anonymized=None):
    users_view.open()
    users_view.create_new_user(user_name, email, first_name, last_name, group, password, view_permissions,
                               timezone, csv_header, csv_delimiter, create_non_anonymized)
    users_view.verify_message('Successfully created user "{}"'.format(user_name))


def delete_user(users_view, username):
    users_view.open()
    users_view.wait_mapping_load()
    users_view.find_and_delete_user_via_delete_operation(username)
    users_view.verify_content_of_delete_confirmation_page(username)
    users_view.confirm_user_delete()
    users_view.wait_mapping_load()
    users_view.verify_message('Successfully deleted user')
    users_view.verify_user_deleted(username)


def delete_report(reports_view, description):
    reports_view.open()
    reports_view.wait_reports_entries_load()
    reports_view.search_and_delete_report(description)


def modify_user_over_users_section(users_view, old_username, new_username, new_password, new_email=None,
                                   new_first_name=None,
                                   new_last_name=None, new_group=None, new_view_permissions=None,
                                   new_timezone='Europe/Berlin',
                                   csv_header=None, csv_delimiter=',', create_non_anonymized=None):
    users_view.open()
    users_view.find_and_modify_user_via_edit_operation(old_username)
    users_view.modify_existing_user(new_username, new_email, new_first_name, new_last_name, new_group,
                                    new_view_permissions,
                                    new_timezone, csv_header, csv_delimiter, create_non_anonymized)
    users_view.wait_mapping_load()
    users_view.verify_message('Successfully updated user "{}"'.format(new_username))
    if new_password:
        users_view.find_and_modify_user_via_edit_operation(new_username)
        driver = users_view.get_driver()
        logged_in_user = users_view.get_logged_in_user()
        if new_username in logged_in_user or (new_first_name and new_last_name in logged_in_user):
            users_view.change_password(new_password)
            login.verify_login_page_open(driver)
            login.login(driver, new_username, new_password)
        else:
            users_view.change_password(new_password)


def create_report(reports_view_object, create_reports_view_object, pcaps_list=None, anonymize_report=None,
                  description=None,
                  report_form_number=1, username=None, groupname=None):
    reports_view_object.open()
    reports_view_object.create()
    create_reports_view_object.fill_report_form_by_form_number(pcaps_list, anonymize_report, description,
                                                               report_form_number, username, groupname)
    create_reports_view_object.create_report_button()
    create_reports_view_object.wait_upload_modal_disappears()


def create_reports(reports_view_object, create_reports_view_object, anonymize_reports_list=None, descriptions_list=None,
                   users_list=None,
                   groups_list=None, pcaps_list=None):
    reports_view_object.open()
    reports_view_object.create()
    create_reports_view_object.fill_bulk_reports_forms(anonymize_reports_list, descriptions_list, users_list,
                                                       groups_list, pcaps_list)
    create_reports_view_object.create_report_button()
    create_reports_view_object.wait_upload_modal_disappears()


def open_report(reports_view_object, report_description):
    reports_view_object.open()
    reports_view_object.search_and_open_report(report_description)


def verify_own_report_actions(all_calls, report_description, anonymized=None, delete=True):
    all_calls.open()
    if not anonymized:
        all_calls.edit_report(report_description)
        all_calls.verify_download_merged_pcap_enabed_and_download_works()
        all_calls.verify_download_original_pcaps_enabed_and_download_works()
        all_calls.verify_mos_file_upload_enabled()
        all_calls.verify_mos_file_download_disabled()
        all_calls.verify_delete_report_enabled()
    elif anonymized:
        all_calls.edit_report(report_description)
        all_calls.verify_download_merged_pcaps_disabled()
        all_calls.verify_download_original_pcap_disabled()
        all_calls.verify_mos_file_upload_disabled()
        all_calls.verify_mos_file_download_disabled()
        all_calls.verify_delete_report_enabled()
    if delete:
        all_calls.delete_report()
        all_calls.confirm_delete_report()


def verify_user_can_create_non_anonymized_reports(reports_view, create_reports_view, non_anonymize_option_enabled):
    if non_anonymize_option_enabled:
        reports_view.open()
        reports_view.create()
        create_reports_view.verify_anonymized_enabled_click_unclick_checkbox()
    elif not non_anonymize_option_enabled:
        reports_view.open()
        reports_view.create()
        create_reports_view.verify_anonymized_disabled_label_appear()


def check_viewing_permissions_and_restrictions_on_report(kpis_objects, can_view_sip_call_id=False,
                                                         can_view_sip_from_to_p_asserted=False,
                                                         can_view_ua_types=False,
                                                         can_view_ip_address=False,
                                                         can_view_ims_node_names=False):
    """
    Functions takes either a single permission to verify on or multiple permissions to verify on.

    :param kpis_objects: a dictionary of all report level and call level kpis objects
    :param allowed_permissions_dict_key_1: str Dictionary key to extract list of allowed table headers
    :param allowed_permissions_dict_key_2: str Dictionary key to extract list of allowed table headers
    :param allowed_permissions_dict_key_3: str Dictionary key to extract list of allowed table headers
    :param allowed_permissions_dict_key_4: str Dictionary key to extract list of allowed table headers
    :param allowed_permissions_dict_key_5: str Dictionary key to extract list of allowed table headers
    """
    key1, key2, key3, key4, key5 = '', '', '', '', ''

    if can_view_sip_call_id:
        key1 = 'Can view SIP Call-ID'
    if can_view_sip_from_to_p_asserted:
        key2 = 'Can view SIP From, To and the P-Asserted-Identity headers'
    if can_view_ua_types:
        key3 = 'Can view UA types'
    if can_view_ip_address:
        key4 = 'Can view IP addresses'
    if can_view_ims_node_names:
        key5 = 'Can view IMS node names'

    error = list()
    for kpi in kpis_objects['Report Level'].values():
        kpi.open()
        try:
            kpi.verify_permissions(kpi.possible_permissions_dict.get(key1) +
                                   kpi.possible_permissions_dict.get(key2) +
                                   kpi.possible_permissions_dict.get(key3) +
                                   kpi.possible_permissions_dict.get(key4) +
                                   kpi.possible_permissions_dict.get(key5))
        except Exception as e:
            error.append(e)
    for kpi in kpis_objects['Call Level'].values():
        kpi.open()
        try:
            kpi.verify_permissions(kpi.possible_permissions_dict.get(key1) +
                                   kpi.possible_permissions_dict.get(key2) +
                                   kpi.possible_permissions_dict.get(key3) +
                                   kpi.possible_permissions_dict.get(key4) +
                                   kpi.possible_permissions_dict.get(key5))
        except Exception as e:
            error.append(e)
    if error:
        for e in error:
            print(e)
        raise AssertionError('Permissions not applied propery! Check printed error messages!')


def create_superuser_and_logout(django_admin_view, username, password):
    django_admin_view.open()
    django_admin_view.create_superuser(username, password)
    django_admin_view.logout()


def delete_user_via_django_admin(django_admin_view, username):
    django_admin_view.open()
    django_admin_view.delete_user(username)


def unblock_and_delete_acess_logs_for_user(django_admin_view, username):
    django_admin_view.open()
    django_admin_view.unblock_user(username)
    django_admin_view.switch_to_view_site()


def reset_failed_logins_after_succesfull_login(driver, username, correct_password):
    for attempt in range(4):
        login.login(driver, username, 'Wrong Password')
        login.verify_failed_login(driver)
    login.login(driver, username, correct_password)
    logout.logout(driver)
    for attempt in range(2):
        login.login(driver, username, 'Wrong Password')
        login.verify_failed_login(driver)
    login.login(driver, username, correct_password)
    login.verify_successfull_login(driver)


def block_user_after_5_failed_logins(driver, username):
    for i in range(5):
        login.login(driver, username, 'WrongPassword')
    login.verify_account_blocked(driver)


def verify_user_blocked_when_logging_in_with_wrong_password(users_view, django_admin_view, username_to_create, password,
                                                            user_type_admin=False,
                                                            user_type_superuser=False):
    driver = users_view.get_driver()
    if user_type_superuser:
        create_superuser_and_logout(django_admin_view, username_to_create, password)
    elif user_type_admin:
        create_user(users_view, username_to_create, None, None, None, 'admin', password)
        logout.logout(driver)
    else:
        create_user(users_view, username_to_create, None, None, None, None, password)
        logout.logout(driver)
    reset_failed_logins_after_succesfull_login(driver, username_to_create, password)
    logout.logout(driver)
    block_user_after_5_failed_logins(driver, username_to_create)
    # Clean Up
    login.login(driver, superuser, superuser_password)
    unblock_and_delete_acess_logs_for_user(django_admin_view, username_to_create)
    logout.logout(driver)
    login.login(driver, username_to_create, password)
    login.verify_successfull_login(driver)
    logout.logout(driver)
    login.login(driver, superuser, superuser_password)
    if user_type_superuser:
        delete_user_via_django_admin(django_admin_view, username_to_create)
        django_admin_view.switch_to_view_site()
    else:
        delete_user(users_view, username_to_create)


def verify_dtag_password_policy_adhered(users_view, django_admin_view, my_profile_View, username_to_create,
                                        password_for_new_user, user_type_admin=False, user_type_superuser=False):
    driver = users_view.get_driver()
    if user_type_superuser:
        create_superuser_and_logout(django_admin_view, username_to_create, password_for_new_user)
        login.login(driver, username_to_create, password_for_new_user)
    elif user_type_admin:
        create_user(users_view, username_to_create, None, None, None, 'admin', password_for_new_user)
        logout.logout(driver)
        login.login(driver, username_to_create, password_for_new_user)
    else:
        create_user(users_view, username_to_create, None, None, None, None, password_for_new_user)
        logout.logout(driver)
        login.login(driver, username_to_create, password_for_new_user)
    # Enter and repeat the current password and verify message
    change_password_verify_change_message(my_profile_View, password_for_new_user,
                                          '×\nThe entered password must be different from the current password')
    # Enter and repeat the exact username as a password
    change_password_verify_change_message(my_profile_View, username_to_create,
                                          '×\nThe password is too similar to the username.')
    # Enter and repeat the part of the username as a password
    change_password_verify_change_message(my_profile_View, username_to_create[:4],
                                          '×\nThe password is too similar to the username.'
                                          '\nThis password is too short. '
                                          'It must contain at least 8 characters.'
                                          '\nYour password must contain at least 3 of the following: '
                                          '1. lowercase character 2. uppercase character '
                                          '3. special character 4. numerical character')

    # Enter and repeat 'Hello' as a password
    change_password_verify_change_message(my_profile_View, 'Hello', '×\nThis password is too short. '
                                                                    'It must contain at least 8 characters.'
                                                                    '\nThis password is too common.'
                                                                    '\nYour password must contain at least 3 of the following: '
                                                                    '1. lowercase character 2. uppercase character '
                                                                    '3. special character 4. numerical character')
    # Enter and repeat 'HelloWorld' as a password
    change_password_verify_change_message(my_profile_View, 'HelloWorld',
                                          '×\nYour password must contain at least 3 of the following: '
                                          '1. lowercase character 2. uppercase character '
                                          '3. special character 4. numerical character')
    # Enter and repeat 'HelloWorld!' as a password
    change_password_verify_change_message(my_profile_View, 'HelloWorld!')
    login.login(driver, username_to_create, 'HelloWorld!')
    # Enter and repeat 'HelloWorld1' as a password
    change_password_verify_change_message(my_profile_View, 'HelloWorld1')
    login.login(driver, username_to_create, 'HelloWorld1')
    # Clean up - reset password
    my_profile_View.open()
    my_profile_View.change_password(password_for_new_user)
    login.login(driver, username_to_create, password_for_new_user)
    logout.logout(driver)
    login.login(driver, superuser, superuser_password)
    delete_user_via_django_admin(django_admin_view, username_to_create)
    unblock_and_delete_acess_logs_for_user(django_admin_view, username_to_create)
    login.login(driver, superuser, superuser_password)
    login.verify_successfull_login(driver)


def change_password_verify_change_message(profile_obj, new_password, change_message=None):
    profile_obj.open()
    # Enter and repeat the current password and verify message
    profile_obj.change_password(new_password)
    if change_message:
        profile_obj.verify_change_password_message(change_message)


def verify_kpis(kpis_objects, testdata_path_dictionary):
    exception_errors = list()
    for kpi in kpis_objects['Report Level'].values():
        kpi.open()
        kpi.download_kpi_as_csv()
        try:
            kpi.compare_csv(testdata_path_dictionary[kpi.__class__.__name__])
        except Exception as e:
            exception_errors.append(e)
    for kpi in kpis_objects['Call Level'].values():
        kpi.open()
        kpi.download_kpi_as_csv()
        try:
            kpi.compare_csv(testdata_path_dictionary[kpi.__class__.__name__])
        except Exception as e:
            exception_errors.append(e)
    if exception_errors:
        [print(e) for e in exception_errors]
        raise Exception('Check Printed messages for Errors')


def apply_filter(all_calls, time_frame=None, start_time=None, end_time=None, n_patterns=None,
                 **percentile):
    all_calls.open()
    all_calls.reset_filters()
    all_calls.filter_by_time_frame(time_frame)
    all_calls.filter_by_start_and_end_time(start_time, end_time)
    all_calls.filter_by_n_patterns(n_patterns)
    all_calls.filter_by_percentile_filter(**percentile)


def upload_download_mos_verify_message_and_kpi(all_calls, mos_file, delimiter='\t', upload=True,
                                               expected_message=None, download_verify_kpi=False):
    all_calls.open()
    if upload:
        all_calls.upload_mos_file_verify_upload_message(mos_file, delimiter, expected_message)
    if download_verify_kpi:
        all_calls.download_mos_file_verify_download(mos_file)


def clean_up_users_and_groups(django_admin_view, groups_view, users_to_not_delete_list=['admin', 'user'],
                              groups_to_not_delete_list=['admin']):
    django_admin_view.open()
    django_admin_view.delete_all_users_except_list(users_to_not_delete_list)
    django_admin_view.unblock_all_users()
    django_admin_view.switch_to_view_site()
    groups_view.open()
    groups_view.delete_all_groups_except_list(groups_to_not_delete_list)


def is_running_in_jenkins():
    pwd = os.path.abspath(os.curdir)
    if ('jenkins' or 'workspace') in pwd:
        return True
    return False


def kill_browsers_processes(pid=None):
    if pid:
        os.system('kill {}'.format(pid))
        return
    os.system('pkill firefox')
    os.system('pkill chrome')
