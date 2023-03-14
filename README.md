# This Repository is only for Uniberg Internal USE ONLY!!!!
## SETA Frontend automation

This automation is done using selenium and UnitTest and is written in Python 3.6.5.

## Requirements Installation

After setting up your virtual environment exceute the following commands

```bash
pip install -r requirements.txt
```

## Download latest version of Firefox and Chrome driver and link them to the right location:

```bash
webdrivermanager firefox chrome 

```

## Add PCAPs, Testdata and Original IP Mappings and Interface Configurations files

```

You should add the following PCAP file to "Data/Testdata/":
1- 1st call.pcapng
2- Test5_Advanced.pcap
3- Test6_Advanced.pcap
4- Test8_Advanced.pcap
5- Test9_Wireshark_filteredX.pcapng
```

```

The Original IP Mappings and Interface Configurations should be added to "Data/OriginalConfigurations/" with the following naming:
1- ip_mappings.csv
2- interface_config.csv 
```
```
Add Testdata csvs manually from Testlink or
from the Tester (7z file, password protected), by extracting and replacing the /Data folder

```
