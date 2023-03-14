import os

PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Percentile/Report Level/')
PERCENTILE_CALL_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Percentile/Call Level/')

TIMEFRAME_REPORT_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Time frame/Report Level/')
TIMEFRAME_CALL_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Time frame/Call Level/')

STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                       'Start time End time Call pattern/Report Level/')
STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                     'Start time End time Call pattern/Call Level/')

# Percentile data with 1st_call.pcap unanonymized
# TODO: All Data need to be redownloaded and checked again after bugs ST-952 and ST-963, ST-973 are fixed
# Report Level
# All Calls
PERCENTILE_AC = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'AC.csv'
# Requests and Responses for All Calls
PERCENTILE_RRAC = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'RRAC.csv'
# System Forwarding Time Per Entity
PERCENTILE_SFTPE = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'SFTPE.csv'
# IMS Forwarding Time
PERCENTILE_IFT = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'IFT.csv'
# Response Timer per IMS Entity
PERCENTILE_RTPIE = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'RTPIE.csv'
# Forwarding Time Next Entity per Node
PERCENTILE_FTNEPN = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPN.csv'
# Forwarding Time Next Entity per Entity
PERCENTILE_FTNEPE = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPE.csv'
# System Forwarding Time Summary
PERCENTILE_SFTS = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'SFTS.csv'
# System Processing Time Summary
PERCENTILE_SPTS = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'SPTS.csv'
# System Forwarding Time For Response All Calls
PERCENTILE_SFTFRAC = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'SFTFRAC.csv'
# Session Establishment Time per term. UA Type
PERCENTILE_SETPTU = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'SETPTU.csv'
# Forwarding Time Next Entity for All Calls
PERCENTILE_FTNEFAC = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEFAC.csv'
# KPI Statistics Summary All Calls
PERCENTILE_KSSAC = PERCENTILE_REPORT_LEVEL_CSV_DIR_PATH + 'KSSAC.csv'
# Call Level
PERCENTILE_RR = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'RR.csv'
PERCENTILE_SFT = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'SFT.csv'
PERCENTILE_SFTR = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'SFTR.csv'
PERCENTILE_SPT = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'SPT.csv'
PERCENTILE_FTNE = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'FTNE.csv'
PERCENTILE_KSS = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'KSS.csv'
PERCENTILE_SD = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'SD.csv'
PERCENTILE_ST = PERCENTILE_CALL_LEVEL_CSV_DIR_PATH + 'ST.csv'
# 1st CALL DICTIONARY
percentile_filter_dict = {'AllCalls': PERCENTILE_AC,
                          'ReqResAllCalls': PERCENTILE_RRAC,
                          'SysForwTimePerEnt': PERCENTILE_SFTPE,
                          'ImsForwTime': PERCENTILE_IFT,
                          'ResTimePerImsEnt': PERCENTILE_RTPIE,
                          'ForwTimeNextEntPerNode': PERCENTILE_FTNEPN,
                          'ForwTimeNextEntPerEnt': PERCENTILE_FTNEPE,
                          'SysForwTimeSummary': PERCENTILE_SFTS,
                          'SysProcTimeSummary': PERCENTILE_SPTS,
                          'SysForwTimeForResAllCalls': PERCENTILE_SFTFRAC,
                          'SessEstPerTermUA': PERCENTILE_SETPTU,
                          'ForwTimeNextEntAllCalls': PERCENTILE_FTNEFAC,
                          'ReqRes': PERCENTILE_RR,
                          'SysForwTime': PERCENTILE_SFT,
                          'SysForwTimeForRes': PERCENTILE_SFTR,
                          'SysProcTime': PERCENTILE_SPT,
                          'ForwTimeNextEnt': PERCENTILE_FTNE,
                          'KPIsStatSummary': PERCENTILE_KSS,
                          'SipDialogs': PERCENTILE_SD,
                          'SipTransactions': PERCENTILE_ST}

""" start-end-callpattern data with 1st_call.pcap unanonymized """
# TODO: All Data need to be redownloaded and checked again after bugs ST-952 and ST-963, ST-973 are fixed
# Report Level
# All Calls
STARTTIME_ENDTIME_CALLPATTERN_AC = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'AC.csv'
# Requests and Responses for All Calls
STARTTIME_ENDTIME_CALLPATTERN_RRAC = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'RRAC.csv'
# System Forwarding Time Per Entity
STARTTIME_ENDTIME_CALLPATTERN_SFTPE = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'SFTPE.csv'
# IMS Forwarding Time
STARTTIME_ENDTIME_CALLPATTERN_IFT = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'IFT.csv'
# Response Timer per IMS Entity
STARTTIME_ENDTIME_CALLPATTERN_RTPIE = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'RTPIE.csv'
# Forwarding Time Next Entity per Node
STARTTIME_ENDTIME_CALLPATTERN_FTNEPN = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPN.csv'
# Forwarding Time Next Entity per Entity
STARTTIME_ENDTIME_CALLPATTERN_FTNEPE = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEPE.csv'
# System Forwarding Time Summary
STARTTIME_ENDTIME_CALLPATTERN_SFTS = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'SFTS.csv'
# System Processing Time Summary
STARTTIME_ENDTIME_CALLPATTERN_SPTS = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'SPTS.csv'
# System Forwarding Time For Response All Calls
STARTTIME_ENDTIME_CALLPATTERN_SFTFRAC = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'SFTFRAC.csv'
# Session Establishment Time per term. UA Type
STARTTIME_ENDTIME_CALLPATTERN_SETPTU = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'SETPTU.csv'
# Forwarding Time Next Entity for All Calls
STARTTIME_ENDTIME_CALLPATTERN_FTNEFAC = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'FTNEFAC.csv'
# KPI Statistics Summary All Calls
STARTTIME_ENDTIME_CALLPATTERN_KSSAC = STARTTIME_ENDTIME_CALLPATTERN_REPORT_LEVEL_CSV_DIR_PATH + 'KSSAC.csv'
# Call Level
STARTTIME_ENDTIME_CALLPATTERN_RR = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'RR.csv'
STARTTIME_ENDTIME_CALLPATTERN_SFT = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'SFT.csv'
STARTTIME_ENDTIME_CALLPATTERN_SFTR = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'SFTR.csv'
STARTTIME_ENDTIME_CALLPATTERN_SPT = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'SPT.csv'
STARTTIME_ENDTIME_CALLPATTERN_FTNE = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'FTNE.csv'
STARTTIME_ENDTIME_CALLPATTERN_KSS = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'KSS.csv'
STARTTIME_ENDTIME_CALLPATTERN_SD = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'SD.csv'
STARTTIME_ENDTIME_CALLPATTERN_ST = STARTTIME_ENDTIME_CALLPATTERN_CALL_LEVEL_CSV_DIR_PATH + 'ST.csv'
# 1st CALL DICTIONARY
start_end_callpattern_filter_dict = {'AllCalls': STARTTIME_ENDTIME_CALLPATTERN_AC,
                                     'ReqResAllCalls': STARTTIME_ENDTIME_CALLPATTERN_RRAC,
                                     'SysForwTimePerEnt': STARTTIME_ENDTIME_CALLPATTERN_SFTPE,
                                     'ImsForwTime': STARTTIME_ENDTIME_CALLPATTERN_IFT,
                                     'ResTimePerImsEnt': STARTTIME_ENDTIME_CALLPATTERN_RTPIE,
                                     'ForwTimeNextEntPerNode': STARTTIME_ENDTIME_CALLPATTERN_FTNEPN,
                                     'ForwTimeNextEntPerEnt': STARTTIME_ENDTIME_CALLPATTERN_FTNEPE,
                                     'SysForwTimeSummary': STARTTIME_ENDTIME_CALLPATTERN_SFTS,
                                     'SysProcTimeSummary': STARTTIME_ENDTIME_CALLPATTERN_SPTS,
                                     'SysForwTimeForResAllCalls': STARTTIME_ENDTIME_CALLPATTERN_SFTFRAC,
                                     'SessEstPerTermUA': STARTTIME_ENDTIME_CALLPATTERN_SETPTU,
                                     'ForwTimeNextEntAllCalls': STARTTIME_ENDTIME_CALLPATTERN_FTNEFAC,
                                     'KPIsStatSummAllCalls': STARTTIME_ENDTIME_CALLPATTERN_KSSAC,
                                     'ReqRes': STARTTIME_ENDTIME_CALLPATTERN_RR,
                                     'SysForwTime': STARTTIME_ENDTIME_CALLPATTERN_SFT,
                                     'SysForwTimeForRes': STARTTIME_ENDTIME_CALLPATTERN_SFTR,
                                     'SysProcTime': STARTTIME_ENDTIME_CALLPATTERN_SPT,
                                     'ForwTimeNextEnt': STARTTIME_ENDTIME_CALLPATTERN_FTNE,
                                     'KPIsStatSummary': STARTTIME_ENDTIME_CALLPATTERN_KSS,
                                     'SipDialogs': STARTTIME_ENDTIME_CALLPATTERN_SD,
                                     'SipTransactions': STARTTIME_ENDTIME_CALLPATTERN_ST}
