from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class AllCalls(KPIsReportLevel):
    def initialize_attributes(self):
        self.csv_kpi_name = 'all_calls'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Call ID', 'Actions', 'Time Frame Start', 'Time Frame End', 'Call Start Time',
                                  'Call End Time',
                                  'First Request', 'Final Response', 'P-Asserted-Identity', 'From', 'To', 'SIP Call ID',
                                  'Orig. UA Type', 'Term. UA Type', 'Session\nEstablishment\nTime (s)',
                                  'Session\nRinging\nTime (s)', 'Session\nProcessing\nTime (s)',
                                  'Request\nPacket ID\n(Orig. P-CSCF Gm)',
                                  'Final Response\nPacket ID\n(Orig. P-CSCF Gm)',
                                  'Ringing Response\nPacket ID\n(Orig. P-CSCF Gm)',
                                  'Request\nPacket ID\n(Term. P-CSCF Gm)',
                                  'Response\nPacket ID\n(Term. P-CSCF Gm)']
        self.default_table_headers = self.all_table_headers[1:]
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['From', 'To', 'SIP Call ID', 'Orig. UA Type', 'Term. UA Type']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': ['SIP Call ID'],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': ['P-Asserted-Identity', 'From', 'To'],
                                          'Can view UA types': ['Orig. UA Type', 'Term. UA Type'],
                                          'Can view IP addresses': [],
                                          'Can view IMS node names': [],
                                          'All  Permissions': ['P-Asserted-Identity', 'From', 'To', 'SIP Call ID',
                                                              'Orig. UA Type', 'Term. UA Type'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        all_calls = self.driver.find_element(By.CSS_SELECTOR, 'ul > li[title="All Calls"] > a')
        all_calls.click()
