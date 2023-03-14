from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class KPIsStatSummAllCalls(KPIsReportLevel):

    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'kpi_call_statistic_summary_for_all_calls'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['KPI', 'Average', 'Variance', 'Std. Deviation', 'Minimum', 'Maximum',
                                  '95% Percentile']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
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
                                                  'ul > li[title="KPI Statistic Summary for All Calls"] > a')
        kpi_statistics.click()
