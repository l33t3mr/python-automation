from selenium.webdriver.common.by import By
from ..KPIsCallLevel import KPIsCallLevel


class KPIsStatSummary(KPIsCallLevel):

    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'kpi_call_statistic_summary_table'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['KPI', 'Average', 'Variance', 'Std. Deviation', 'Minimum', 'Maximum',
                                  '95% Percentile (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Request\nNode Name', 'Request\nIP Address', 'Response\nNode Name', 'Response\nIP Address']
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
        self._wait_kpi_table_load()
        kpi_statistics = self.driver.find_element(By.CSS_SELECTOR,
                                                  'ul > li[title="KPI Statistic Summary"] > a')
        kpi_statistics.click()
