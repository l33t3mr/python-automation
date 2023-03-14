from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class ImsForwTime(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'ims_forwarding_time'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Actions', 'Time Frame Start', 'Time Frame End', 'SIP Call ID',
                                  'IMS Forwarding\nTime Request (s)', 'IMS Forwarding\nTime Response (s)',
                                  'IMS Forwarding\nTime Request\nOriginating (s)',
                                  'IMS Forwarding\nTime Request\nTerminating (s)',
                                  'IMS Forwarding\nTime Response\nOriginating (s)',
                                  'IMS Forwarding\nTime Response\nTerminating (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['SIP Call ID']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': ['SIP Call ID'],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': [],
                                          'All  Permissions': ['SIP Call ID'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        for_time_per_iMS = self.driver.find_element(By.CSS_SELECTOR,
                                                    'ul > li[title="IMS Forwarding Time"] > a')
        for_time_per_iMS.click()
