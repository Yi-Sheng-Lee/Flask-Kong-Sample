from enum import Enum


class ReportNameEnum(Enum):
    UNTREATED_INCIDENT_REPORT = "未處理資安事件報表"
    UNTREATED_ACCIDENT_REPORT = "未處理通報單報表"
    SUBMITTED_ACCIDENT_REPORT = "已完成通報通報單報表"


class ReportTemplateEnum(Enum):
    UNTREATED_INCIDENT_REPORT = "report/untreated_incident_report_template.html"
    UNTREATED_ACCIDENT_REPORT = "report/untreated_accident_report_template.html"
    SUBMITTED_ACCIDENT_REPORT = "report/submitted_accident_report_template.html"


class ScheduleReportIntervalCode(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class ConfigGroupCode(Enum):
    HOSTNAME = 'hostname'
    TIMESERVER = 'timeserver'
    SYSTEM = 'system'
    SMTP = 'smtp'
    NETWORK = 'network'
    ORGANIZATION = 'organization'
    NOTIFICATION_INCIDENT = 'notification_incident'


class IncidentHasAccidentCode(Enum):
    ALL = 0
    HAS_ACCIDENT = 1
    NO_ACCIDENT = 2


class AccidentRequireSupportCode(Enum):
    YES = 1
    NO = 0


class AccidentSubmitTargetCode(Enum):
    NCCST = 1
    TWCERT = 2


class CountryCode(Enum):
    UNKNOWN = 'ND'
    INTERNAL_NETWORK = 'ND'


class AvtIntrusionLevel(Enum):
    SYSTEM_COMPROMISE = "System Compromise"
    EXPLOITATION_AND_INSTALLATION = "Exploitation & Installation"
    DELIVERY_AND_ATTACK = "Delivery & Attack"
    RECONNAISSANCE_AND_PROBING = "Reconnaissance & Probing"
    ENVIRONMENTAL_AWARENESS = "Environmental Awareness"


class DeviceRegionLayer(Enum):
    COUNTRY = 1
    CITY = 2
    ZIP = 3
    COMPANY = 4
    SENSOR = 5
    GROUP = 6


class ApiTokenType(Enum):
    ALIENVAULT = "avt"
    MINISOC = "ossim"
    ISAC_WIZARD = "isac"
    LOG_MASTER = "lm"


class SensorType(Enum):
    ALIENVAULT = 'avt'
    LOG_MASTER = "lm"


class DeviceGroupType(Enum):
    OT = 'OT'
    IT = 'IT'
    CUSTOM_01 = 'CUST01'





