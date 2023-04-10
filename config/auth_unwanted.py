"""
功能
    1:USER_MANAGE,
    2:ROLE_MANAGE,
    3:MONITOR_DEVICE_MANAGE,
    4:MONITOR_DEVICE_GROUP_MANAGE,
    5:SYSTEM_CONFIGURE,
    6:DASHBOARD_TEMPLATE_MANAGE,
    7:DASHBOARD
    8:DATA_MIGRATE_MANAGE
    9:COMPANY_MANAGE
    10: SENSOR_MANAGE
    11: INCIDENT_MANAGE
    12: ACCIDENT_MANAGE
    13: ACCIDENT_VERIFY_MANAGE
    14: ACCIDENT_VERIFY_FLOW_MANAGE
    15: STATISTICS_REPORT
    16: SCHEDULE_REPORT_MANAGE
    17: SMTP_CONFIGURE
    18: ACCIDENT_SUBMIT_CONFIGURE
    19: SENTIMENT_MANAGE
    20: PULSE_MANAGE
    21: OPERATION_RECORD_MANAGE
    22: AUDIT_MANAGE
    23: CLAUSE_TYPE_MANAGE
操作
    1: CREATE,
    2: UPDATE,
    3: DELETE,
    4: VIEW,
    5: VERIFY,
    6: EXPORT,
    7: SUBMIT,
    8: DOWNLOAD,
    9: REJECT,
    10: ARCHIVE,
    11: UPLOAD
"""

AUTH_UNWANTED = {
    1: {5, 6, 7, 8, 9, 10, 11},
    2: {5, 6, 7, 8, 9, 10, 11},
    3: {5, 6, 7, 8, 9, 10, 11},
    4: {5, 6, 7, 8, 9, 10, 11},
    5: {1, 3, 5, 6, 7, 8, 9, 10, 11},
    6: {5, 6, 7, 8, 9, 10, 11},
    7: {1, 2, 3, 5, 6, 7, 8, 9, 10, 11},
    8: {1, 3, 5, 6, 7, 8, 9, 10, 11},
    9: {5, 6, 7, 8, 9, 10, 11},
    10: {5, 6, 7, 8, 9, 10, 11},
    11: {5, 6, 9, 11},
    12: {5, 6, 9, 11},
    13: {1, 2, 3, 6, 7, 8, 10, 11},
    14: {5, 6, 7, 8, 9, 10, 11},
    15: {1, 2, 3, 5, 7, 8, 9, 10, 11},
    16: {5, 6, 7, 9, 10, 11},
    17: {1, 3, 5, 6, 7, 8, 9, 10, 11},
    18: {1, 3, 5, 6, 7, 8, 9, 10, 11},
    19: {1, 2, 3, 5, 6, 7, 8, 9, 10, 11},
    20: {5, 6, 7, 8, 9, 10, 11},
    21: {1, 2, 3, 5, 6, 7, 9, 10, 11},
    22: {5, 6, 7, 9, 10},
    23: {5, 6, 7, 8, 9, 10, 11}
}
