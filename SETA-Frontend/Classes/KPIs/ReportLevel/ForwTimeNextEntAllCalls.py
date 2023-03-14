from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class ForwTimeNextEntAllCalls(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'forwarding_time_next_entity_for_all_calls'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Time Frame Start', 'Time Frame End', 'SIP Call ID', 'P-Asserted-Identity', 'From',
                                  'To', 'IMS Entity', 'IMS Entity\nCall Leg', 'Node Name', 'IP Address',
                                  'Incoming\nTime Stamp', 'Incoming\nPacket ID', 'From\nIMS Entity', 'From\nNode',
                                  'From\nInterface', 'From\nProtocol', 'From\nMethod', 'Outgoing\nTime Stamp',
                                  'Outgoing\nPacket ID', 'To\nIMS Entity', 'To\nNode', 'To\nInterface', 'To\nProtocol',
                                  'To\nMethod', 'Forwarding\nTime Next\nEntity (s)']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['SIP Call ID', 'IP Address', 'From\nNode', 'To\nNode', 'Node Name']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': ['SIP Call ID'],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': ['P-Asserted-Identity', 'From', 'To'],
                                          'Can view UA types': [],
                                          'Can view IP addresses': ['IP Address'],
                                          'Can view IMS node names': ['From\nNode', 'To\nNode', 'Node Name'],
                                          'All  Permissions': ['SIP Call ID', 'P-Asserted-Identity', 'From', 'To',
                                                              'IP Address', 'From\nNode', 'To\nNode', 'Node Name'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        forw_time_next_entity = self.driver.find_element(
            By.CSS_SELECTOR, 'ul > li[title="Forwarding Time Next Entity for all Calls"] > a')
        forw_time_next_entity.click()
