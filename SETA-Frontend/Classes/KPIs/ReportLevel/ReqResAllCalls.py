from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class ReqResAllCalls(KPIsReportLevel):
    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'request_response'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Actions', 'Time Frame Start', 'Time Frame End', 'Interface', 'Protocol',
                                  'Duration (s)', 'SIP Call ID', 'P-Asserted-Identity', 'From', 'To', 'Request Time',
                                  'Request\nIMS Entity', 'Request\nIMS Entity\nCall Leg', 'Request\nNode Name',
                                  'Request\nIP Address', 'Request\nMethod', 'Request\nPacket ID', 'Response Time',
                                  'Response\nIMS Entity', 'Response\nIMS Entity\nCall Leg', 'Response\nNode Name',
                                  'Response\nIP Address', 'Response\nMethod', 'Response\nPacket ID']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['From', 'To', 'SIP Call ID', 'Request\nNode Name', 'Request\nIP Address',
        #                    'Response\nNode Name', 'Response\nIP Address']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': ['SIP Call ID'],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': ['P-Asserted-Identity', 'From', 'To'],
                                          'Can view UA types': [],
                                          'Can view IP addresses': ['Response\nIP Address', 'Request\nIP Address'],
                                          'Can view IMS node names': ['Response\nNode Name', 'Request\nNode Name'],
                                          'All  Permissions': ['P-Asserted-Identity', 'From', 'To', 'SIP Call ID',
                                                              'Request\nNode Name', 'Request\nIP Address',
                                                              'Response\nNode Name', 'Response\nIP Address'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        req_resp = self.driver.find_element(By.CSS_SELECTOR,
                                            'ul > li[title="Requests and Responses for All Calls"] > a')
        req_resp.click()
