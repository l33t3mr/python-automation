import unittest
import time
from selenium.webdriver.common.by import By

from Classes.POM import InterfaceConfig
from Modules import login, logout
from Modules.helpers import verify_mapping_upload_succeeded, verify_mapping_upload_fails, \
    verify_cancel_upload_button_works, verify_message_after_adding_entries, \
    verify_entries_get_deleted_successfully
from Modules.authorization_info import url, adminuser, adminuser_password
from Modules.shared_objects import create_firefox_driver
from Data.OriginalConfigurations.OriginalConfigurationsData import original_interface_configuration_csv
from Data.Testdata.InterfaceConfiguration.InterfaceConfigData import *
from Modules.element_attributes import element_is_visible


class InterfaceConfigTests(unittest.TestCase):

    def setUp(self):
        self.driver = create_firefox_driver(url, __name__)
        login.login(self.driver, adminuser, adminuser_password)
        self.interface_config = InterfaceConfig.InterfaceConfig(self.driver)

    def tearDown(self):
        self.interface_config.open()
        if element_is_visible(self.driver, '.modal-footer > .btn.btn-secondary'):
            self.driver.find_element(By.CSS_SELECTOR, '.modal-footer > .btn.btn-secondary').click()
        if element_is_visible(self.driver, '#status-btn-del-pending'):
            self.driver.find_element(By.CSS_SELECTOR, '#status-btn-del-pending').click()
        logout.logout(self.driver)
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.driver = create_firefox_driver(url)
        login.login(cls.driver, adminuser, adminuser_password)
        cls.interface_config = InterfaceConfig.InterfaceConfig(cls.driver)
        verify_mapping_upload_succeeded(cls.interface_config, original_interface_configuration_csv)
        cls.driver.quit()

        '''Path in TestLink: Interface Config -> Delete & Minimum Req. / Need Help?'''

    def test_1(self):  # TCST-252 Deleting: Minimum Req. & Need Help
        self.interface_config.open()
        self.interface_config.delete_all_config()
        self.interface_config.verify_message_delete(
            'Cannot delete interface config (UA, P-CSCF, both, Gm), because deletion would hurt'
            ' the rules for mandatory interfaces. Please check help for more information.')
        self.interface_config.get_help_verify()

    def test_2(self):  # TCST-255 Deleting Interfaces (Single Deletion with "x")
        verify_message_after_adding_entries(self.interface_config, [('TCST', 'TC255', 'Link', 'both')])
        verify_entries_get_deleted_successfully(self.interface_config, [('TCST', 'TC255', 'Link', 'both')])

    def test_3(self):  # TCST-256 Deleting Interfaces (Bulk Delete)
        verify_message_after_adding_entries(self.interface_config, [('Node1', 'Test1', 'Interface1', 'outgoing'),
                                                                    ('Node2', 'Test2', 'Interface2', 'incoming')])

        verify_entries_get_deleted_successfully(self.interface_config,
                                                [('Node1', 'Test1', 'Interface1', 'outgoing'),
                                                 ('Node2', 'Test2', 'Interface2', 'incoming')], True)

    '''Path in Testlink: Interface Config -> IC - Valid Input'''

    def test_4(self):  # TCST-262 Uploading valid CSV[clear pending process]
        verify_cancel_upload_button_works(self.interface_config, TCST_262_CSV)

    def test_5(self):  # Restore Config
        verify_mapping_upload_succeeded(self.interface_config, original_interface_configuration_csv)

    def test_6(self):  # TCST-372 Uploading CSV file with Header/Delimiter ","
        verify_mapping_upload_succeeded(self.interface_config, TCST_372_CSV)

    def test_7(self):  # TCST-373 Uploading CSV file without Header/Delimiter ","
        verify_mapping_upload_succeeded(self.interface_config, TCST_373_CSV, csv_header_enabled=False)

    def test_8(self):  # TCST-374 Uploading CSV file with delimiter ";"
        verify_mapping_upload_succeeded(self.interface_config, TCST_374_CSV, ';')

    def test_9(self):  # TCST-375 Downloading Interface Config Mappings as CSV
        self.interface_config.open()
        self.interface_config.download_mapping()

    def test_10(self):  # TCST-376 Entering Relations manually
        verify_message_after_adding_entries(self.interface_config,
                                            [('XXX', 'YYY', 'CCC', 'outgoing'), ('XXX', 'YYY', 'CCC', 'incoming'),
                                             ('AAA', 'BBB', 'XXX', 'both'), ('DDD', 'EEE', 'FFF', 'outgoing')])
        verify_entries_get_deleted_successfully(self.interface_config,
                                                [('XXX', 'YYY', 'CCC', 'outgoing'), ('XXX', 'YYY', 'CCC', 'incoming'),
                                                 ('AAA', 'BBB', 'XXX', 'both'), ('DDD', 'EEE', 'FFF', 'outgoing')],
                                                True)

        '''Path In TestLink: Interface Config -> IC - Invalid Input -> IC -CSVs -> Logic'''

    def test_11(self):  # TCST-266 : FIRST Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_266_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_12(self):  # TCST-267 : SECOND Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_267_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_13(self):  # TCST-269 : THIRD Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_269_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_14(self):  # TCST-271 : FOURTH Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_271_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_15(self):  # TCST-273 : FIFTH Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_273_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_16(self):  # TCST-275 : SIXTH Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_275_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_17(self):  # TCST-277 : SEVENTH Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_277_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_18(self):  # TCST-279 : EIGHTH Adding Duplicate Interfaces (csv)
        verify_mapping_upload_fails(self.interface_config, TCST_279_CSV,
                                    expected_fail_message="Direction: Value 'y' is not a valid choice.")

    def test_19(self):  # TCST-258 : Uploading CSV file with Duplicates
        verify_mapping_upload_fails(self.interface_config, TCST_258_ONE_DUPLICATE_CSV,
                                    expected_fail_message='Conflicting interface configurations are already defined between'
                                                          ' node "98821ss" and node "76hxv0".')
        verify_mapping_upload_fails(self.interface_config, TCST_258_TWO_DUPLICATE_CSV,
                                    expected_fail_message='Conflicting interface configurations are already defined between'
                                                          ' node "98821ss" and node "76hxv0".')

        ''' Interface Config -> IC - Invalid Input -> IC -CSVs -> input fields and format'''

    def test_20(self):  # TCST-264 : Uploading CSV file with invalid direction
        verify_mapping_upload_fails(self.interface_config, TCST_264_CSV,
                                    expected_fail_message="Direction: Value 'UP' is not a valid choice.")

    def test_21(self):  # TCST-377 : Uploading CSV with extra Cols[clear failed uploads]
        verify_mapping_upload_fails(self.interface_config, TCST_377_CSV,
                                    expected_fail_message='CSV must have exactly 4 columns! '
                                                          '[First node, Second node, Direction, Interface]')

    def test_22(self):  # TCST-378 : Uploading CSV with missing Col
        verify_mapping_upload_fails(self.interface_config, TCST_378_CSV,
                                    expected_fail_message='CSV must have exactly 4 columns! '
                                                          '[First node, Second node, Direction, Interface]')

    def test_23(self):  # TCST-380 : Uploading CSV without mandatory Interface Conf.
        verify_mapping_upload_fails(self.interface_config, TCST_380_CSV,
                                    expected_fail_message='Please make sure the uploaded configurations contain all '
                                                          'mandatory interfaces. Click on "Need help?" for more'
                                                          ' information')

    def test_24(self):  # TCST-381 : Uploading non-CSV file
        verify_mapping_upload_fails(self.interface_config, TCST_381_SH, expected_fail_message='file must be csv')

    def test_25(self):  # TCST-387 : Empty Input
        verify_mapping_upload_fails(self.interface_config, TCST_387_FILL_FILL_EMPTY_CSV,
                                    expected_fail_message='Interface name: This field cannot be blank.')

        verify_mapping_upload_fails(self.interface_config, TCST_387_FILL_EMPTY_EMPTY_CSV,
                                    expected_fail_message='Second node: This field cannot be blank. Interface name: This field cannot be '
                                                          'blank.')

        verify_mapping_upload_fails(self.interface_config, TCST_387_EMPTY_FILL_FILL_CSV,
                                    expected_fail_message='First node: This field cannot be blank.')

        verify_mapping_upload_fails(self.interface_config, TCST_387_EMPTY_FILL_EMPTY_CSV,
                                    expected_fail_message='Interface name: This field cannot be blank. First node: This field cannot be '
                                                          'blank.')

        verify_mapping_upload_fails(self.interface_config, TCST_387_EMPTY_EMPTY_FILL_CSV,
                                    expected_fail_message='Second node: This field cannot be blank. First node: This field cannot be blank.')

        verify_mapping_upload_fails(self.interface_config, TCST_387_EMPTY_EMPTY_EMPTY_CSV,
                                    expected_fail_message='Second node: This field cannot be blank.'
                                                          ' Interface name: This field cannot be blank.'
                                                          ' First node: This field cannot be blank.', )

        verify_mapping_upload_fails(self.interface_config, TCST_387_FILL_FILL_SPACE_CSV,
                                    expected_fail_message='Cannot save blank fields')

        verify_mapping_upload_fails(self.interface_config, TCST_387_FILL_SPACE_FILL_CSV,
                                    expected_fail_message='Cannot save blank fields')

        verify_mapping_upload_fails(self.interface_config, TCST_387_SPACE_FILL_FILL_CSV,
                                    expected_fail_message='Cannot save blank fields')

    '''Path In TestLink: Interface Config -> IC - Invalid Input -> IC - Manual Input -> Logic'''

    def test_26(self):  # TCST-265 FIRST Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'outgoing')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_27(self):  # TCST-268 SECOND Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'incoming')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_28(self):  # TCST-270 THIRD Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'incoming'), ('x', 'z', 'y', 'both')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_29(self):  # TCST-272 FOURTH Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'outgoing'), ('x', 'z', 'y', 'both')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_30(self):  # TCST-274 FIFTH Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'outgoing'), ('x', 'z', 'y', 'incoming'),
                                             ('x', 'z', 'y', 'both')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_31(self):  # TCST-276 SIXTH Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'outgoing'),
                                             ('x', 'z', 'y', 'incoming')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_32(self):  # TCST-278 SEVENTH Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'incoming'),
                                             ('x', 'z', 'y', 'outgoing')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_33(self):  # TCST-280 EIGHTH Adding Duplicate Interfaces
        verify_message_after_adding_entries(self.interface_config,
                                            [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'outgoing'),
                                             ('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'outgoing')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "x" and node "z".')

    def test_34(self):  # TCST-382 Duplicate Configuration (exists in the Mapping already)
        verify_mapping_upload_succeeded(self.interface_config, original_interface_configuration_csv)
        verify_message_after_adding_entries(self.interface_config, [('UA', 'P-CSCF', 'Gm', 'both')],
                                            'Conflicting interface configurations are already defined between'
                                            ' node "UA" and node "P-CSCF".')

    def test_35(self):  # TCST-383 Duplicate Configuration in the input itself)
        verify_mapping_upload_succeeded(self.interface_config, original_interface_configuration_csv)
        verify_message_after_adding_entries(self.interface_config, [('x', 'z', 'y', 'both'), ('x', 'z', 'y', 'both')],
                                            'Conflicting interface configurations are already defined'
                                            ' between node "x" and node "z".')

    '''Path In TestLink: Interface Config -> IC - Invalid Input -> IC - Manual Input -> Input fields and format'''

    def test_36(self):  # TCST-386 Empty Input
        # empty,empty,empty
        verify_message_after_adding_entries(self.interface_config, [('', '', '', 'both')], 'No data to submit!')

        # empty,empty,fill
        verify_message_after_adding_entries(self.interface_config, [('', '', 'x', 'outgoing')],
                                            'Second node: This field cannot be blank.'
                                            '\nFirst node: This field cannot be blank.')

        # empty,fill,empty
        verify_message_after_adding_entries(self.interface_config, [('', 'x', '', 'incoming')],
                                            'Interface name: This field cannot be blank.'
                                            '\nFirst node: This field cannot be blank.')
        # empty,fill,fill
        verify_message_after_adding_entries(self.interface_config, [('', 'x', 'c', 'both')],
                                            'First node: This field cannot be blank.')

        # fill,empty,empty
        verify_message_after_adding_entries(self.interface_config, [('x', '', '', 'both')],
                                            'Interface name: This field cannot be blank.'
                                            '\nSecond node: This field cannot be blank.')

        # fill,fill,empty
        verify_message_after_adding_entries(self.interface_config, [('x', 'c', '', 'both')],
                                            'Interface name: This field cannot be blank.')

        # fill,fill,space
        verify_message_after_adding_entries(self.interface_config, [('x', 'c', ' ', 'both')],
                                            'Interface name: This field cannot be blank.')

    def test_37(self):  # TCST-511 : Deleting: Obligate the user to have a UA in the interface configurations
        self.interface_config.open()
        self.interface_config.wait_for_add_entry_table_to_load()
        self.interface_config.delete_entries([('UA', 'P-CSCF', 'Gm', 'both')])
        self.interface_config.verify_message_delete(
            'Cannot delete interface config (UA, P-CSCF, both, Gm), because deletion would hurt'
            ' the rules for mandatory interfaces. Please check help for more information.')

        verify_message_after_adding_entries(self.interface_config, [('test36', 'UA', 'Gm', 'both')])
        verify_entries_get_deleted_successfully(self.interface_config, [('UA', 'P-CSCF', 'Gm', 'both')])

        self.interface_config.delete_entries([('test36', 'UA', 'Gm', 'both')])
        self.interface_config.verify_message_delete(
            'Cannot delete interface config (test36, UA, both, Gm), because deletion would hurt'
            ' the rules for mandatory interfaces. Please check help for more information.')

        verify_message_after_adding_entries(self.interface_config, [('UA', 'P-CSCF', 'Gm', 'both')])
        verify_entries_get_deleted_successfully(self.interface_config, [('test36', 'UA', 'Gm', 'both')])

    # tcst_263 (search functionality) : the search function is used in some methods, this tcst is not needed here


if __name__ == '__main__':
    unittest.main()
