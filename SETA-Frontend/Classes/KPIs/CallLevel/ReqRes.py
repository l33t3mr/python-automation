from selenium.webdriver.common.by import By
from ..KPIsCallLevel import KPIsCallLevel


class ReqRes(KPIsCallLevel):

    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'requests_and_responses'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['Interface', 'Protocol', 'Duration (s)', 'Request Time', 'Transaction ID',
                                  'Request Time', 'SIP Dialog Call ID', 'Request\nIMS Entity',
                                  'Request\nIMS Entity\nCall Leg', 'Request\nNode Name', 'Request\nIP Address',
                                  'Request\nMethod', 'Request\nPacket ID', 'Response Time', 'Response\nIMS Entity',
                                  'Response\nIMS Entity\nCall Leg', 'Response\nNode Name', 'Response\nIP Address',
                                  'Response\nMethod', 'Response\nPacket ID']
        self.default_table_headers = self.all_table_headers
        self.default_columns_dropdown = self.all_table_headers
        # all cols that can be restricted
        # All  Permissions = ['Request\nNode Name', 'Request\nIP Address', 'Response\nNode Name', 'Response\nIP Address']
        # No Permissions = []
        # possible allowed cols
        self.possible_permissions_dict = {'Can view SIP Call-ID': [],
                                          'Can view SIP From, To and the P-Asserted-Identity headers': [],
                                          'Can view UA types': [],
                                          'Can view IP addresses': ['Request\nIP Address', 'Response\nIP Address'],
                                          'Can view IMS node names': ['Request\nNode Name', 'Response\nNode Name'],
                                          'All  Permissions': ['Request\nNode Name', 'Request\nIP Address',
                                                              'Response\nNode Name',
                                                              'Response\nIP Address'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        req_res = self.driver.find_element(By.CSS_SELECTOR,
                                           'ul > li[title="Requests and Responses"] > a')
        req_res.click()
