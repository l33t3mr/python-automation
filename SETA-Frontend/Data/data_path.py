import os

TESTDATA_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Testdata/')
DOWNLOAD_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Downloads/')

RANDOM_CSV = TESTDATA_DIR_PATH + 'random.csv'
FIRST_CALL_PCAP = TESTDATA_DIR_PATH + '1st call.pcapng'
ERICSSON_ERICSSON_PCAP = TESTDATA_DIR_PATH + 'Ericsson_Ericsson.pcap'
MOS_CLABOR_PACP = TESTDATA_DIR_PATH + 'MOS CLABOR.pcap'
TEST5_ADVANCED_PACP = TESTDATA_DIR_PATH + 'Test5_Advanced.pcap'
TEST6_ADVANCED_PCAP = TESTDATA_DIR_PATH + 'Test6_Advanced.pcap'
TEST8_ADVANCED_PCAP = TESTDATA_DIR_PATH + 'Test8_Advanced.pcap'
TEST9_WIRESHARK_FILTERED_PCAP = TESTDATA_DIR_PATH + 'Test9_Wireshark_filtered.pcapng'