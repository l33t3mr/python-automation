from selenium.webdriver.common.by import By
from ..KPIsCallLevel import KPIsCallLevel


class SipTransactions(KPIsCallLevel):

    def initialize_attributes(self):
        # Class Attributes
        # CSV name
        self.csv_kpi_name = 'sip_tramsactions'
        # Default Table Headers in an ordered way
        self.all_table_headers = ['SIP Transaction ID', 'Number of Requests', 'Number of Responses',
                                  'Transaction Initiating Node Name', 'Transaction Initiating Node Type',
                                  'Transaction Ending Node Name', 'Transaction Ending Node Type']
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
                                          'Can view IMS node names': ['Transaction Initiating Node Name',
                                                                'Transaction Ending Node Name'],
                                          'All  Permissions': ['Transaction Initiating Node Name',
                                                              'Transaction Ending Node Name'],
                                          'No Permissions': [],
                                          '': []
                                          }

    def open(self):
        super()._open()
        sip_transactions = self.driver.find_element(By.CSS_SELECTOR,
                                                    'ul > li[title="SIP Transactions"] > a')
        sip_transactions.click()
