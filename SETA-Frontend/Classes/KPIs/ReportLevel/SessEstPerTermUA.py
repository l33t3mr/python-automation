from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class SessEstPerTermUA(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'session_establishment_times_term_ua'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Time Frame Start', 'Time Frame End', 'Term. UA Type', 'Presence\nin Calls',
                                  'Average Session\nEstablishment\nTime (s)',
                                  'Variance\nin Session\nEstablishment\nTime (s)',
                                  'Std. Deviation\nin Session\nEstablishment\nTime (s)',
                                  'Minimum Session\nEstablishment\nTime (s)',
                                  'Maximum Session\nEstablishment\nTime (s)',
                                  '95% Percentile\nof Establishment\nTime (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Term. UA Type']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': [],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': ['Term. UA Type'],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': [],
                                          'All  Permissions': ['Term. UA Type'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        sess_per_ua = self.driver.find_element(By.CSS_SELECTOR,
                                               'ul > li[title="Session Establishment Time per term. UA Type"] > a')
        sess_per_ua.click()
