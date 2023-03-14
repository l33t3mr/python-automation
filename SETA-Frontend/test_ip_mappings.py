import unittest

from selenium.webdriver.common.by import By

from Classes.POM import IpMappings
from Modules import login, logout
from Modules.authorization_info import url, adminuser, adminuser_password
from Modules.shared_objects import create_firefox_driver
from Modules.helpers import verify_mapping_upload_succeeded, verify_mapping_upload_fails, \
    verify_message_after_adding_entries, verify_entries_get_deleted_successfully
from Modules.element_attributes import element_is_visible
from Data.Testdata.IpMapping.IpMappingData import *
from Data.OriginalConfigurations.OriginalConfigurationsData import original_ip_mapping_csv


class IpMappingsTests(unittest.TestCase):

    def setUp(self):
        # cls.times_driver_used = 0
        self.driver = create_firefox_driver(url, __name__)
        login.login(self.driver, adminuser, adminuser_password)
        self.ip_mappings = IpMappings.IpMappings(self.driver)
        self.ip_mappings.open()
        if element_is_visible(self.driver, '#status-btn-del-pending'):
            self.ip_mappings.clear_failed_uploads_or_cancel_pending_uploads()

    def tearDown(self):
        # if Upload Modal is visible, close
        if element_is_visible(self.driver, '.modal-footer > .btn.btn-secondary'):
            self.driver.find_element(By.CSS_SELECTOR, '.modal-footer > .btn.btn-secondary').click()
        # if there's upload pending/failed upload, clear it.
        if element_is_visible(self.driver, '#status-btn-del-pending'):
            self.driver.find_element(By.CSS_SELECTOR, '#status-btn-del-pending').click()
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.driver = create_firefox_driver(url)
        login.login(cls.driver, adminuser, adminuser_password)
        cls.ip_mappings = IpMappings.IpMappings(cls.driver)
        verify_mapping_upload_succeeded(cls.ip_mappings, original_ip_mapping_csv)
        cls.driver.quit()

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - Manual Input -> Logic -> IPv6'''

    def test_1(self):  # TCST-329 Duplicate Node/IP address (in the Input itself)
        verify_message_after_adding_entries(self.ip_mappings,
                                            [('TestNode1', 'P-CSCF', '20DD::1'), ('TestNode1', 'S-CSCF', '20DD::1')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", it already has the type "P-CSCF",'
                                            'Duplicated IP Address: 20dd::1 already exists. An IP address can only occur once in '
                                            'the IP Mappings.')

    def test_2(self):  # TCST-330 Duplicate Node/IP address (exists in IP Mappings already)
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', '50DD::1')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', '50DD::1')],
                                            'Duplicated IP Address: 20dd::1 already exists. '
                                            'An IP address can only occur once in the IP Mappings.')
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode1', 'P-CSCF', '50DD::1')])

    def test_3(self):  # TCST-331  A Node can't have two different node types (in the input itself)
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', 'DDD::A'),
                                                               ('TestNode1', 'S-CSCF', 'DDD::B')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", '
                                            'it already has the type "P-CSCF"')

    def test_4(self):  # TCST-332 : A Node can't have two different node types (exists in the IP Mappings already)
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', 'AAAA::1')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'S-CSCF', 'BBBB::2')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", '
                                            'it already has the type "P-CSCF"')
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode1', 'P-CSCF', 'AAAA::1')])

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - Manual Input -> Logic -> IPv4'''

    def test_5(self):  # TCST-324 : Duplicate Node/IP address(in the Input itself)
        verify_message_after_adding_entries(self.ip_mappings,
                                            [('TestNode1', 'P-CSCF', '1.1.1.1'), ('TestNode1', 'S-CSCF', '1.1.1.1')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", it already has the type'
                                            ' "P-CSCF",Duplicated IP Address: 1.1.1.1 already exists. An IP address '
                                            'can only occur once in the IP Mappings.')

    def test_6(self):  # TCST-235 : Duplicate Node/IP Address(exists in IP Mappings already)
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', '1.1.1.1')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', '1.1.1.1')],
                                            'Duplicated IP Address: 1.1.1.1 already exists. '
                                            'An IP address can only occur once in the IP Mappings.')

    def test_7(self):  # TCST-236 : A Node can't have two different node types (in the input itself)
        verify_message_after_adding_entries(self.ip_mappings,
                                            [('TestNode1', 'P-CSCF', '1.1.1.1'), ('TestNode1', 'S-CSCF', '2.2.2.2')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", '
                                            'it already has the type "P-CSCF"')

    def test_8(self):  # TCST-325 : A Node can't have two different node types (exists in the IP Mappings already)
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'P-CSCF', '1.1.1.1')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode1', 'S-CSCF', '2.2.2.2')],
                                            'Cannot assign type "S-CSCF" for node "TestNode1", '
                                            'it already has the type "P-CSCF"')
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode1', 'P-CSCF', '1.1.1.1')])

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - Manual Input -> input fields and format'''

    def test_9(self):  # TCST-366 : IPv4 Validation
        # Extra Octet
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2.3.4.5')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # Missing Octet
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2.3')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # Changing Dot Seperator
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1:2:3:4')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # Negative values
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.-2.3.4')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # More than 3 digits
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2444.3.4')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # None-Numbers
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2.3.#')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # None-Numbers & Digit
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2.3.3#')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # No Prefix
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1.2.3.0/16')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

    def test_10(self):  # TCST-367 : IPv6 Validation
        # Extra Nibble
        verify_message_after_adding_entries(self.ip_mappings,
                                            [('x', 'y', '1200:0000:AB00:1234:0000:2552:7777:1313:AAAA')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Missing Nibble
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200:0000:AB00:1234:0000:2552:7777')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Extra Hex Char
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200:0000:AB00:1234:0000:2552:7777:131AB')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Changing Double Points Separator
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200,0000:AB00:1234:0000:2552:7777:131A')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Negative Values
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '-1200:0000:AB00:1234:0000:2552:7777:131A')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Only Two Double Points are allowed 
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200:0000:AB00:1234:0000::2552::131A')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Special Symbols
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200:0000:AB00:1234:0000:2552:7777:131!')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

        # Exceeding Hex Value
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200:0000:AB00:1234:0000:2552:7777:131L')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')
        # No Prefix
        verify_message_after_adding_entries(self.ip_mappings, [('x', 'y', '1200::1/128')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.')

    def test_11(self):  # TCST-370 : Empty Input & Mix Invalid IP
        # empty,empty,empty
        verify_message_after_adding_entries(self.ip_mappings, [('', '', '')], 'No data to submit!')

        # empty,empty,fill
        verify_message_after_adding_entries(self.ip_mappings, [('', '', '3.3.3.3')],
                                            'Node name: This field cannot be blank.'
                                            '\nIms entity: This field cannot be blank.')

        # empty,fill,empty
        verify_message_after_adding_entries(self.ip_mappings, [('', 'x', '')],
                                            'Node name: This field cannot be blank.'
                                            '\nIp address: This field cannot be blank.')

        # empty,fill,fill
        verify_message_after_adding_entries(self.ip_mappings, [('', 'x', '3.3.3.3')],
                                            'Node name: This field cannot be blank.')

        # fill,empty,empty
        verify_message_after_adding_entries(self.ip_mappings, [('y', '', '')],
                                            'Ip address: This field cannot be blank.'
                                            '\nIms entity: This field cannot be blank.')

        # fill,fill,empty
        verify_message_after_adding_entries(self.ip_mappings, [('y', 'x', '')],
                                            'Ip address: This field cannot be blank.')

        # fill, empty, fill
        verify_message_after_adding_entries(self.ip_mappings, [('y', '', '3.3.3.3')],
                                            'Ims entity: This field cannot be blank.')

        # empty, empty, wrong IP
        verify_message_after_adding_entries(self.ip_mappings, [('', '', '3.3.3.3.3')],
                                            'Node name: This field cannot be blank.'
                                            '\nIp address: Enter a valid IPv4 or IPv6 address.'
                                            '\nIms entity: This field cannot be blank.')

        # empty, fill, wrong IP
        verify_message_after_adding_entries(self.ip_mappings, [('', 'x', '3.3.3.3.3')],
                                            'Node name: This field cannot be blank.'
                                            '\nIp address: Enter a valid IPv4 or IPv6 address.')

        # fill, empty, wrong IP
        verify_message_after_adding_entries(self.ip_mappings, [('y', '', '3.3.3.3.3')],
                                            'Ip address: Enter a valid IPv4 or IPv6 address.'
                                            '\nIms entity: This field cannot be blank.')

        # fill, space, valid IP
        verify_message_after_adding_entries(self.ip_mappings, [('y', ' ', '1.1.1.1')],
                                            'Ims entity: This field cannot be blank.')

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - CSVs -> logic -> IPv4'''

    def test_12(self):  # TCST-234 : Uploading CSV file with Duplicate IPs
        verify_mapping_upload_fails(self.ip_mappings, TCST_234_ONE_DUPLICATE_CSV,
                                    expected_fail_message='Duplicated IP Address: 10.0.12.130 already exists. '
                                                          'An IP address can only occur once in the IP Mappings.')
        verify_mapping_upload_fails(self.ip_mappings, TCST_234_TWO_DUPLICATE_CSV,
                                    expected_fail_message='Duplicated IP Address: 10.0.12.130 already exists. '
                                                          'An IP address can only occur once in the IP Mappings.')

    def test_13(self):  # TCST-342 : A Node can't have two different node types
        verify_mapping_upload_fails(self.ip_mappings, TCST_342_CSV,
                                    expected_fail_message='Cannot assign type "S-CSCF" for node "TestNode42", '
                                                          'it already has the type "P-CSCF"')

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - CSVs -> logic -> IPv6'''

    def test_14(self):  # TCST-361 : Uploading CSV file with Duplicate IPs
        verify_mapping_upload_fails(self.ip_mappings, TCST_361_ONE_DUPLICATE_csv,
                                    expected_fail_message='Duplicated IP Address: 2a01:598:4:4003::8 already exists.'
                                                          ' An IP address can only occur once in the IP Mappings.')
        verify_mapping_upload_fails(self.ip_mappings, TCST_361_TWO_DUPLICATE_CSV,
                                    expected_fail_message='Duplicated IP Address: 2a01:598:4:4004::4 already exists.'
                                                          ' An IP address can only occur once in the IP Mappings.')

    def test_15(self):  # TCST-362 : A Node can't have two different node types
        verify_mapping_upload_fails(self.ip_mappings, TCST_362_CSV,
                                    expected_fail_message='Cannot assign type "S-CSCF" for node "TestNode62", '
                                                          'it already has the type "P-CSCF"')

    '''Path in TestLink: Ip Mapping -> IM - Invalid Input -> IM - CSVs -> input fields and format'''

    # TODO: def test_51(self):  # TCST-388 : Save without selecting CSV file   [must be automated for both IP and IC]

    def test_16(self):  # TCST-233 : Uploading CSV[Header functionality/CSV Columns]
        verify_mapping_upload_fails(self.ip_mappings, TCST_233_BAD_HEADER_2_COLS_CSV,
                                    expected_fail_message='CSV must have exactly 3 columns! '
                                                          '[Node name, IMS entity, IP address]',
                                    csv_header_enabled=False)
        verify_mapping_upload_fails(self.ip_mappings, TCST_233_BAD_HEADER_4_COLS_CSV,
                                    expected_fail_message='CSV must have exactly 3 columns! '
                                                          '[Node name, IMS entity, IP address]',
                                    csv_header_enabled=False)

    def test_17(self):  # TCST-248 : Uploading non-CSV file
        verify_mapping_upload_fails(self.ip_mappings, TCST_248_SH, expected_fail_message='file must be csv')

    def test_18(self):  # TCST-368 : IPv4 Validation
        # Extra Octet
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_EXTRA_OCTET_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Missing Octet
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_MISSING_OCTET_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Changing Dot Separator
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_CHANGING_DOT_SEPARATOR_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Negative value
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_NEGATIVE_VALUE_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # More than 3 digits
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_MORE_THAN_3_DIGITS_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # None Numbers
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_NON_NUMBERS_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # None Numbers & Digits
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_NON_NUMBERS_AND_DIGITS_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # No Prefix
        verify_mapping_upload_fails(self.ip_mappings, TCST_368_NO_PREFIX,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

    def test_19(self):  # TCST-369 : IPv6 Validation
        # Extra Nibble
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_EXTRA_NIBBLE_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Missing Nibble
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_MISSING_NIBBLE_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Extra Hex Char
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_EXTRA_HEX_CHAR_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Negative value
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_NEGATIVE_VALUES,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Only Two doubel points allowed
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_ONLY_TWO_DOUBLE_POINTS_ARE_ALLOWED_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Special Symbols
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_SPECIAL_SYMBOLS_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Exceeding Hex value
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_EXCEEDING_HEX_VALUE_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # No Prefix
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_NO_PREFIX_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

        # Change separator
        verify_mapping_upload_fails(self.ip_mappings, TCST_369_CHANGING_DOUBLE_POINTS_SEPARATOR_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address.')

    def test_20(self):  # TCST-371 : Empty Input & Mix Invalid IP
        # empty,empty,empty
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_EMPTY_EMPTY_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank.'
                                                          ' Ip address: This field cannot be blank. '
                                                          'Node name: This field cannot be blank.')  # Bug Ticket ST-794
        # fill,empty,fill
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_EMPTY_FILL_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank.')

        # fill,fill,empty
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_FILL_EMPTY_CSV,
                                    expected_fail_message='Ip address: This field cannot be blank.')

        # empty, fill, fill
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_FILL_FILL_CSV,
                                    expected_fail_message='Node name: This field cannot be blank.')

        # empty, empty, wrong ip
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_EMPTY_WRONG_IP_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank. Ip address: '
                                                          'Enter a valid IPv4 or IPv6 address.'
                                                          ' Node name: This field cannot be blank.')

        # empty, fill, wrong ip
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_FILL_WRONG_IP_CSV,
                                    expected_fail_message='Ip address: Enter a valid IPv4 or IPv6 address. '
                                                          'Node name: This field cannot be blank.')

        # fill, empty, wrong ip
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_EMPTY_WRONG_IP_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank. '
                                                          'Ip address: Enter a valid IPv4 or IPv6 address.')
        # fill, empty, empty
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_EMPTY_EMPTY_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank.'
                                                          ' Ip address: This field cannot be blank.')
        # empty, fill, empty
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_FILL_EMPTY_CSV,
                                    expected_fail_message='Ip address: This field cannot be blank. '
                                                          'Node name: This field cannot be blank.')
        # empty, empty, fill
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_EMPTY_EMPTY_FILL_CSV,
                                    expected_fail_message='Ims entity: This field cannot be blank.'
                                                          ' Node name: This field cannot be blank.')
        # fill, fill, space
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_FILL_SPACE_CSV,
                                    expected_fail_message='Ip address: This field cannot be blank.')
        # fill, space, fill
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_FILL_SPACE_FILL_CSV,
                                    expected_fail_message='Cannot save blank fields')
        # space, fill, fill
        verify_mapping_upload_fails(self.ip_mappings, TCST_371_SPACE_FILL_FILL_CSV,
                                    expected_fail_message='Cannot save blank fields')

    '''Path in TestLink: Ip Mapping -> IM - valid Input -> IM - CSVs -> IM - CSVs IPv4'''

    def test_21(self):  # TCST-344 : A Node and its Node Type can have different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_344_CSV)

    def test_22(self):  # TCST-345 : Different Nodes with the same Node type & different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_345_CSV)

    def test_23(self):  # TCST-346 : Different Nodes & different Node type & different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_346_CSV)

    '''Path in TestLink: Ip Mapping -> IM - valid Input -> IM - CSVs -> IM - CSVs IPv6'''

    def test_24(self):  # TCST-363 : A Node and its Node Type can have different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_363_CSV)

    def test_25(self):  # TCST-364 : Different Nodes with the same Node type & different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_364_CSV)

    def test_26(self):  # TCST-365 : Different Nodes & different Node type & different IPs
        verify_mapping_upload_succeeded(self.ip_mappings, TCST_365_CSV)

    '''Path in TestLink: Ip Mapping -> IM - valid Input -> IM - CSVs '''

    # TCST-365 covered in tearDownClass

    '''Path in TestLink: Ip Mapping -> IM - valid Input -> IM - Manual Input -> IM - IPv4 -> valid input'''

    def test_27(self):  # TCST-326 : A Node and its Node Type can have different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode2', 'P-CSCF', '3.3.3.3')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode2', 'P-CSCF', '2.2.2.2')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode2', 'P-CSCF', '3.3.3.3'),
                                                                   ('TestNode2', 'P-CSCF', '2.2.2.2')])

    def test_28(self):  # TCST-327 : Different Nodes with the same Node type & different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode5', 'P-CSCF', '5.5.5.5'),
                                                               ('TestNode6', 'P-CSCF', '6.6.6.6')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode5', 'P-CSCF', '5.5.5.5'),
                                                                   ('TestNode6', 'P-CSCF', '6.6.6.6')])

    def test_29(self):  # TCST-328 : Different Nodes & different Node type & different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode7', 'P-CSCF', '7.7.7.7'),
                                                               ('TestNode8', 'S-CSCF', '8.8.8.8')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode7', 'P-CSCF', '7.7.7.7'),
                                                                   ('TestNode8', 'S-CSCF', '8.8.8.8')])

    '''Path in TestLink: Ip Mapping -> IM - valid Input -> IM - Manual Input -> IM - IPv6 -> valid input'''

    def test_30(self):  # TCST-333 : A Node and its Node Type can have different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode2', 'P-CSCF', 'CCCC::C')])
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode2', 'P-CSCF', 'BBBB::B')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode2', 'P-CSCF', 'CCCC::C'),
                                                                   ('TestNode2', 'P-CSCF', 'BBBB::B')])

    def test_31(self):  # TCST-334 : Different Nodes with the same Node type & different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode5', 'P-CSCF', 'EEEE::E'),
                                                               ('TestNode6', 'P-CSCF', 'EEAA::E')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode5', 'P-CSCF', 'EEEE::E'),
                                                                   ('TestNode6', 'P-CSCF', 'EEAA::E')])

    def test_32(self):  # TCST-335 : Different Nodes & different Node type & different IPs
        verify_message_after_adding_entries(self.ip_mappings, [('TestNode7', 'P-CSCF', 'BBAA::A'),
                                                               ('TestNode8', 'S-CSCF', 'BBDD::D')])
        verify_entries_get_deleted_successfully(self.ip_mappings, [('TestNode7', 'P-CSCF', 'BBAA::A'),
                                                                   ('TestNode8', 'S-CSCF', 'BBDD::D')])

    '''Path in TestLink: Ip Mapping ->  Delete & Minimum Req. / Need Help?'''

    def test_33(self):  # Deleting: Minimum Req. & Need Help
        ip = IpMappings.IpMappings(self.driver)
        ip.open()
        ip.delete_all_config()
        ip.get_help_verify()

    '''Path in TestLink: Ip Mapping'''

    def test_34(self):  # TCST-20 : Settings / IP Mappings ["Download IP mappings"]
        ip = IpMappings.IpMappings(self.driver)
        ip.open()
        ip.download_mapping()

    #     # TCST-238, TCST-237, TCST-249 are already covered in other tests


if __name__ == '__main__':
    unittest.main()
