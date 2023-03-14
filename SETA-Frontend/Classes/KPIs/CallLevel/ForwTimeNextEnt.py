from selenium.webdriver.common.by import By
from ..KPIsCallLevel import KPIsCallLevel


class ForwTimeNextEnt(KPIsCallLevel):

    def initialize_attributes(self):
        # CSV name
        self.csv_kpi_name = 'forwarding_time_next_entity'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['IMS Entity', 'IMS Entity\nCall Leg', 'Node Name', 'IP Address',
                                  'Incoming\nTime Stamp', 'Incoming\nPacket ID', 'From\nIMS Entity', 'From\nNode',
                                  'From\nInterface', 'From\nProtocol', 'From\nMethod', 'Outgoing\nTime Stamp',
                                  'Outgoing\nPacket ID', 'To\nIMS Entity', 'To\nNode', 'To\nInterface', 'To\nProtocol',
                                  'To\nMethod', 'Forwarding\nTime Next\nEntity (s)']
        self.default_table_headers = self.all_table_headers

        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Node Name', 'IP Address', 'From\nNode', 'To\nNode']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': [],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': ['IP Address'],
                                          'Can view IMS node names': ['Node Name', 'From\nNode', 'To\nNode'],
                                          'All  Permissions': ['Node Name', 'IP Address', 'From\nNode', 'To\nNode'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        forw_time = self.driver.find_element(By.CSS_SELECTOR,
                                             'ul > li[title="Forwarding Time Next Entity"] > a')
        forw_time.click()
