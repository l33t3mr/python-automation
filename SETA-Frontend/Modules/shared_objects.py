from Classes.POM import *
from Classes.KPIs.CallLevel import *
from Classes.KPIs.ReportLevel import *
from .initialize_webdriver import ff_webdriver
from Modules.helpers import is_running_in_jenkins


def create_kpi_objects(driver):
    kpis_objects_report_level = {
        'AllCalls': AllCalls.AllCalls(driver),
        'ReqResAllCalls': ReqResAllCalls.ReqResAllCalls(driver),
        'SysForwTimePerEnt': SysForwTimePerEnt.SysForwTimePerEnt(driver),
        'ImsForwTime': ImsForwTime.ImsForwTime(driver),
        'ResTimePerImsEnt': ResTimePerImsEnt.ResTimePerImsEnt(driver),
        'ForwTimeNextEntPerNode': ForwTimeNextEntPerNode.ForwTimeNextEntPerNode(driver),
        'ForwTimeNextEntPerEnt': ForwTimeNextEntPerEnt.ForwTimeNextEntPerEnt(driver),
        'SysForwTimeSummary': SysForwTimeSummary.SysForwTimeSummary(driver),
        'SysProcTimeSummary': SysProcTimeSummary.SysProcTimeSummary(driver),
        'SysForwTimeForRespAllCalls': SysForwTimeForResAllCalls.SysForwTimeForResAllCalls(driver),
        'SessEstPerTermUA': SessEstPerTermUA.SessEstPerTermUA(driver),
        'ForwTimeNextEntAllCalls': ForwTimeNextEntAllCalls.ForwTimeNextEntAllCalls(driver),
        'KPIsStatSummAllCalls': KPIsStatSummAllCalls.KPIsStatSummAllCalls(driver)}
    kpis_objects_call_level = {
        'ReqRes': ReqRes.ReqRes(driver, kpis_objects_report_level['AllCalls']),
        'SysForwTime': SysForwTime.SysForwTime(driver, kpis_objects_report_level['AllCalls']),
        'SysForwTimeForRes': SysForwTimeForRes.SysForwTimeForRes(driver,
                                                                 kpis_objects_report_level['AllCalls']),
        'SysProcTime': SysProcTime.SysProcTime(driver, kpis_objects_report_level['AllCalls']),
        'ForwTimeNextEnt': ForwTimeNextEnt.ForwTimeNextEnt(driver, kpis_objects_report_level['AllCalls']),
        'KPIsStatSummary': KPIsStatSummary.KPIsStatSummary(driver, kpis_objects_report_level['AllCalls']),
        'SipDialogs': SipDialogs.SipDialogs(driver, kpis_objects_report_level['AllCalls']),
        'SipTransactions': SipTransactions.SipTransactions(driver, kpis_objects_report_level['AllCalls'])}
    return {'Report Level': kpis_objects_report_level, 'Call Level': kpis_objects_call_level}


def create_groups_view(driver):
    return Groups.Groups(driver)


def create_users_view(driver):
    return Users.Users(driver)


def create_interface_config_view(driver):
    return InterfaceConfig.InterfaceConfig(driver)


def create_ip_mappings_view(driver):
    return IpMappings.IpMappings(driver)


def create_reports_view(driver):
    return ReportsView.ReportsView(driver)


def create_create_reports_view(driver):
    return CreateReport.CreateReport(driver)


def create_django_admin_view(driver):
    return DjangoAdmin.DjangoAdmin(driver)


def create_my_profile_view(driver):
    return MyProfile.MyProfile(driver)


def create_firefox_driver(url, log_name=None, headless=False):
    if is_running_in_jenkins():
        return ff_webdriver(url, log_name, True)
    if headless:
        return ff_webdriver(url, log_name, True)
    return ff_webdriver(url, log_name)
