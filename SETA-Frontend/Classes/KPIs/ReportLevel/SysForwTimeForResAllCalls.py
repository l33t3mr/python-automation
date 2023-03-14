from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class SysForwTimeForResAllCalls(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'system_forwarding_time_responses_all_calls'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Time Frame Start', 'Time Frame End', 'SIP Call ID', 'IMS Entity',
                                  'IMS Entity Call Leg', 'Node Name', 'Forwarded Response Method',
                                  'Associated Request Method', 'Forwarding Time\nfor Response (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Node Name']
        # no_permission = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': ['SIP Call ID'],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': ['Node Name'],
                                          'All  Permissions': ['Node Name', 'SIP Call ID'],
                                          'no_permission': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        # open KPI
        sys_forw = self.driver.find_element(By.CSS_SELECTOR,
                                            'ul > li[title="System Forwarding Time For Response All Calls"] > a')
        sys_forw.click()
