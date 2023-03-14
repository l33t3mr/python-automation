from selenium.webdriver.common.by import By
from ..KPIsCallLevel import KPIsCallLevel


class SysProcTime(KPIsCallLevel):

    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'system_processing_times'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['IMS Entity', 'IMS Entity Call Leg', 'Node Name', 'Processing Time (s)']
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
        sys_for = self.driver.find_element(By.CSS_SELECTOR,
                                           'ul > li[title="System Processing Time"] > a')
        sys_for.click()
