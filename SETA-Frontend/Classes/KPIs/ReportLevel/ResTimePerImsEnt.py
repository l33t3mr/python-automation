from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class ResTimePerImsEnt(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'response_time_per_entity'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Time Frame Start', 'Time Frame End', 'IMS Entity', 'IMS Entity\nCall Leg',
                                  'Presence\nin Calls', 'Average\nResponse\nTime (s)',
                                  'Variance\nin Response\nTime (s)',
                                  'Std. Deviation\nin Response\nTime (s)', 'Minimum\nResponse\nTime (s)',
                                  'Maximum\nResponse\nTime (s)', '95% Percentile\nof Response\nTime (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = []
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': [],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': [],
                                          'All  Permissions': [],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        for_time_per_node = self.driver.find_element(By.CSS_SELECTOR,
                                                     'ul > li[title="Response Time per IMS Entity"] > a')
        for_time_per_node.click()
