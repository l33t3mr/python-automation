from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class SysForwTimeSummary(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'system_forwarding_time_summary'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Time Frame Start', 'Time Frame End', 'IMS Entity', 'IMS Entity\nCall Leg',
                                  'Node Name', 'Forwarded Request Method', 'Presence\nin Calls',
                                  'Average\nForwarding\nTime (s)', 'Variance\nin Forwarding\nTime (s)',
                                  'Std. Deviation\nin Forwarding\nTime (s)', 'Minimum\nForwarding\nTime (s)',
                                  'Maximum\nForwarding\nTime (s)', '95% Percentile\nof Forwarding\nTime (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Node Name']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': [],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': ['Node Name'],
                                          'All  Permissions': ['Node Name'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        sys_forw_time_summary = self.driver.find_element(By.CSS_SELECTOR,
                                                         'ul > li[title="System Forwarding Time Summary"] > a')
        sys_forw_time_summary.click()
