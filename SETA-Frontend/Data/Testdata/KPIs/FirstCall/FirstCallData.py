import os

ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                    'Anonymized/Report Level/')
ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Anonymized/Call Level/')

NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                        'Non-Anonymized/Report Level/')
NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                      'Non-Anonymized/Call Level/')

""" 1st_call.pacp Non-Anonymized """
# TODO: All Data need to be redownloaded and checked again after bugs ST-952 and ST-963 are fixed
# Report Level
# All Calls
NON_ANONYMIZED_AC = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'AC.csv'
# Requests and Responses for All Calls
NON_ANONYMIZED_RRAC = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'RRAC.csv'
# System Forwarding Time Per Entity
NON_ANONYMIZED_SFTPE = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTPE.csv'
# IMS Forwarding Time
NON_ANONYMIZED_IFT = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'IFT.csv'
# Response Timer per IMS Entity
NON_ANONYMIZED_RTPIE = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'RTPIE.csv'
# Forwarding Time Next Entity per Node
NON_ANONYMIZED_FTNEPN = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPN.csv'
# Forwarding Time Next Entity per Entity
NON_ANONYMIZED_FTNEPE = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPE.csv'
# System Forwarding Time Summary
NON_ANONYMIZED_SFTS = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTS.csv'
# System Processing Time Summary
NON_ANONYMIZED_SPTS = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SPTS.csv'
# System Forwarding Time For Response All Calls
NON_ANONYMIZED_SFTFRAC = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTFRAC.csv'
# Session Establishment Time per term. UA Type
NON_ANONYMIZED_SETPTU = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SETPTU.csv'
# Forwarding Time Next Entity for All Calls
NON_ANONYMIZED_FTNEFAC = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEFAC.csv'
# KPI Statistics Summary All Calls
NON_ANONYMIZED_KSSAC = NON_ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'KSSAC.csv'
# Call Level
NON_ANONYMIZED_RR = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'RR.csv'
NON_ANONYMIZED_SFT = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SFT.csv'
NON_ANONYMIZED_SFTR = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SFTR.csv'
NON_ANONYMIZED_SPT = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SPT.csv'
NON_ANONYMIZED_FTNE = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'FTNE.csv'
NON_ANONYMIZED_KSS = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'KSS.csv'
NON_ANONYMIZED_SD = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SD.csv'
NON_ANONYMIZED_ST = NON_ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'ST.csv'
# 1st CALL DICTIONARY
non_anonymized_dict = {'AllCalls': NON_ANONYMIZED_AC,
                       'ReqResAllCalls': NON_ANONYMIZED_RRAC,
                       'SysForwTimePerEnt': NON_ANONYMIZED_SFTPE,
                       'ImsForwTime': NON_ANONYMIZED_IFT,
                       'ResTimePerImsEnt': NON_ANONYMIZED_RTPIE,
                       'ForwTimeNextEntPerNode': NON_ANONYMIZED_FTNEPN,
                       'ForwTimeNextEntPerEnt': NON_ANONYMIZED_FTNEPE,
                       'SysForwTimeSummary': NON_ANONYMIZED_SFTS,
                       'SysProcTimeSummary': NON_ANONYMIZED_SPTS,
                       'SysForwTimeForResAllCalls': NON_ANONYMIZED_SFTFRAC,
                       'SessEstPerTermUA': NON_ANONYMIZED_SETPTU,
                       'ForwTimeNextEntAllCalls': NON_ANONYMIZED_FTNEFAC,
                       'KPIsStatSummAllCalls': NON_ANONYMIZED_KSSAC,
                       'ReqRes': NON_ANONYMIZED_RR,
                       'SysForwTime': NON_ANONYMIZED_SFT,
                       'SysForwTimeForRes': NON_ANONYMIZED_SFTR,
                       'SysProcTime': NON_ANONYMIZED_SPT,
                       'ForwTimeNextEnt': NON_ANONYMIZED_FTNE,
                       'SipDialogs': NON_ANONYMIZED_SD,
                       'KPIsStatSummary': NON_ANONYMIZED_KSS,
                       'SipTransactions': NON_ANONYMIZED_ST}

""" 1st_call.pacp Anonymized """
# TODO: All Data need to be redownloaded and checked again after bugs ST-952 and ST-963, ST-973 are fixed
# Report Level
# All Calls
ANONYMIZED_AC = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'AC.csv'
# Requests and Responses for All Calls
ANONYMIZED_RRAC = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'RRAC.csv'
# System Forwarding Time Per Entity
ANONYMIZED_SFTPE = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTPE.csv'
# IMS Forwarding Time
ANONYMIZED_IFT = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'IFT.csv'
# Response Timer per IMS Entity
ANONYMIZED_RTPIE = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'RTPIE.csv'
# Forwarding Time Next Entity per Node
ANONYMIZED_FTNEPN = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPN.csv'
# Forwarding Time Next Entity per Entity
ANONYMIZED_FTNEPE = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPE.csv'
# System Forwarding Time Summary
ANONYMIZED_SFTS = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTS.csv'
# System Processing Time Summary
ANONYMIZED_SPTS = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SPTS.csv'
# System Forwarding Time For Response All Calls
ANONYMIZED_SFTFRAC = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SFTFRAC.csv'
# Session Establishment Time per term. UA Type
ANONYMIZED_SETPTU = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'SETPTU.csv'
# Forwarding Time Next Entity for All Calls
ANONYMIZED_FTNEFAC = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEFAC.csv'
# KPI Statistics Summary All Calls
ANONYMIZED_KSSAC = ANONYMIZED_REPORT_LEVEL_CSV_DIR_PATH + 'KSSAC.csv'
# Call Level
ANONYMIZED_RR = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'RR.csv'
ANONYMIZED_SFT = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SFT.csv'
ANONYMIZED_SFTR = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SFTR.csv'
ANONYMIZED_SPT = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SPT.csv'
ANONYMIZED_FTNE = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'FTNE.csv'
ANONYMIZED_KSS = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'KSS.csv'
ANONYMIZED_SD = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'SD.csv'
ANONYMIZED_ST = ANONYMIZED_CALL_LEVEL_CSV_DIR_PATH + 'ST.csv'
# 1st CALL DICTIONARY
anonymized_dict = {'AllCalls': ANONYMIZED_AC,
                   'ReqResAllCalls': ANONYMIZED_RRAC,
                   'SysForwTimePerEnt': ANONYMIZED_SFTPE,
                   'ImsForwTime': ANONYMIZED_IFT,
                   'ResTimePerImsEnt': ANONYMIZED_RTPIE,
                   'ForwTimeNextEntPerNode': ANONYMIZED_FTNEPN,
                   'ForwTimeNextEntPerEnt': ANONYMIZED_FTNEPE,
                   'SysForwTimeSummary': ANONYMIZED_SFTS,
                   'SysProcTimeSummary': ANONYMIZED_SPTS,
                   'SysForwTimeForResAllCalls': ANONYMIZED_SFTFRAC,
                   'SessEstPerTermUA': ANONYMIZED_SETPTU,
                   'ForwTimeNextEntAllCalls': ANONYMIZED_FTNEFAC,
                   'KPIsStatSummAllCalls': ANONYMIZED_KSSAC,
                   'ReqRes': ANONYMIZED_RR,
                   'SysForwTime': ANONYMIZED_SFT,
                   'SysForwTimeForRes': ANONYMIZED_SFTR,
                   'SysProcTime': ANONYMIZED_SPT,
                   'ForwTimeNextEnt': ANONYMIZED_FTNE,
                   'KPIsStatSummary': ANONYMIZED_KSS,
                   'SipDialogs': ANONYMIZED_SD,
                   'SipTransactions': ANONYMIZED_ST}
