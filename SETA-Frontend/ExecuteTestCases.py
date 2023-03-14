import pytest
from Modules.helpers import kill_browsers_processes, clean_up_users_and_groups, is_running_in_jenkins
from Modules.authorization_info import url, superuser, superuser_password
from Modules import login
from Modules.shared_objects import create_django_admin_view, create_groups_view, create_firefox_driver
from PytestReportsHelpers.PytestHTMLReportsMerger import HTMLMerger, XMLMerger

single_workers = 1
parallel_workers = 4
if is_running_in_jenkins():
    parallel_workers = 6

if __name__ == '__main__':
    print('Cleaning Up Users and Groups')
    driver = create_firefox_driver(url, __name__)
    django_admin_view = create_django_admin_view(driver)
    groups_view = create_groups_view(driver)
    login.login(driver, superuser, superuser_password)
    clean_up_users_and_groups(django_admin_view, groups_view)
    driver.quit()
    kill_browsers_processes()
    print('Finished Cleaning UP')

    pytest.main(
        ['-n={}'.format(parallel_workers), '-v', '--tb=short', '--durations=20',
         '--junitxml=./Reports/CreateNewReports.xml',
         '--html=./Reports/CreateNewReports.html', '--self-contained-html', 'test_create_new_report.py'])

    kill_browsers_processes()

    pytest.main(
        ['-n={}'.format(single_workers), '-v', '--tb=short', '--durations=20',
         '--junitxml=./Reports/InterfaceConfig.xml',
         '--html=./Reports/InterfaceConfig.html', '--self-contained-html', 'test_interface_config.py'])

    kill_browsers_processes()

    pytest.main(
        ['-n={}'.format(single_workers), '-v', '--tb=short', '--durations=20', '--junitxml=./Reports/IpMappings.xml',
         '--html=./Reports/IpMappings.html', '--self-contained-html', 'test_ip_mappings.py'])

    kill_browsers_processes()

    pytest.main(
        ['-n={}'.format(parallel_workers), '-v', '--tb=short', '--durations=20', '--junitxml=./Reports/Report.xml',
         '--html=./Reports/Report.html', '--self-contained-html', 'test_report.py'])

    kill_browsers_processes()

    pytest.main(
        ['-n={}'.format(parallel_workers), '-v', '--tb=short', '--durations=20',
         '--junitxml=./Reports/ShareReportAndReportOptions.xml',
         '--html=./Reports/ShareReportAndReportOptions.html', '--self-contained-html',
         'test_share_report_and_report_options.py'])

    kill_browsers_processes()

    pytest.main(
        ['-n={}'.format(parallel_workers), '-v', '--tb=short', '--durations=20',
         '--junitxml=./Reports/UsersManagementAndRights.xml',
         '--html=./Reports/UsersManagementAndRights.html', '--self-contained-html',
         'test_users_management_and_rights.py'])
    kill_browsers_processes()
    #
    merge_html_report = HTMLMerger('./Reports/CreateNewReports.html', './Reports/InterfaceConfig.html',
                                   './Reports/IpMappings.html', './Reports/Report.html',
                                   './Reports/ShareReportAndReportOptions.html',
                                   './Reports/UsersManagementAndRights.html')
    merge_html_report.create_merged_xml('./Reports/Merged_Report.html')

    merge_xml_report = XMLMerger('./Reports/CreateNewReports.html', './Reports/InterfaceConfig.xml',
                                 './Reports/IpMappings.xml', './Reports/Report.xml',
                                 './Reports/ShareReportAndReportOptions.xml',
                                 './Reports/UsersManagementAndRights.xml')
    merge_html_report.create_merged_xml('./Reports/Merged_Report.xml')

