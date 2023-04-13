import os
from config.task_config import JOBS as task_jobs
import common.util.encrypted_util as encrypted


class BaseConfig(object):
    # Service
    DEBUG = False
    PORT = 8088
    HOST = "0.0.0.0"
    TOKEN_TTL = 3600
    # SERVER_NAME = "localhost:8089"

    # Base app path
    # APPLICATION_ROOT = "/api/1.0"

    SCHEDULE_REPORT_PATH = "file/pdf/"
    STIX_FILE_PATH = "file/stix/"
    TWCERT_FILE_PATH = "file/eml/"
    RECORD_FILE_PATH = "file/record/"
    SENSOR_TMP_FILE_PATH = "file/sensor/"

    # EXCEPTION
    PROPAGATE_EXCEPTIONS = True

    # MariaDB
    DB_DB = os.getenv("DB_DB") or "mssp"
    DB_USER = os.getenv("DB_USER") or "msspmgr"
    DB_HOST = os.getenv("DB_HOST") or "192.168.69.194"
    DB_PORT = os.getenv("DB_PORT") or "5005"
    # encrypted.encodeData_test("sqlcode", "billows12345")
    DB_CODE = encrypted.getDecodeCode_test("sqlcode")

    # SQLAlchemy
    SQLALCHEMY_POOL_RECYCLE = 540
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_CODE}@{DB_HOST}:{DB_PORT}/{DB_DB}"
    )

    # Logging
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "./log/mssp/mssp-api.log"

    # Netplan
    NETPLAN_LOCATION = "/etc/netplan/00-installer-config.yaml"
    NETPLAN_INTERFACE = "ens160"

    # Timeserver
    NTP_LOCATION = "/etc/systemd/timesyncd.conf"

    # JWT
    # JWT_SECRET_KEY = "rse"
    JWT_SECRET_KEY = "this is mssp product"
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = 3000
    JWT_REFRESH_TOKEN_EXPIRES = 7200
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # kong
    KONG_URL = "192.168.69.194"

    # Reqparse
    BUNDLE_ERRORS = True

    # Wkhtmltopdf
    WKHTMLTOPDF_BIN_PATH = '/usr/local/bin/wkhtmltopdf'
    PDF_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')
    # Flask-APSchedule
    SCHEDULER_API_ENABLED = True
    JOBS = task_jobs

    # GeoIP2 Databases Path
    GEOIP2_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'lib/geoip2/GeoLite2-City.mmdb')

    # REDIS
    REDIS_HOST = os.getenv("REDDIS_HOST") or "192.168.69.194"
    REDIS_AVT_DB = 0
    
    # 將密碼加密成binary file
    # encrypted.encodeData_test("rediscode", "billows12345")
    REDIS_PWD = encrypted.getDecodeCode_test("rediscode")

    # TWCERT Submit MAIL
    TWCERT_EMAIL = "twcert@cert.org.tw"
    CLAUSEFILE_HOME = "./clausefile/"


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    # Service
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8088
    # SERVER_NAME = "192.168.66.81:8089"

    # MariaDB
    DB_USER = os.getenv("DB_USER") or "msspmgr"
    # encrypted.encodeData_test("sqlcode", "billows12345")
    # DB_CODE = encrypted.getDecodeCode_test("sqlcode")


    # DB_DB = os.getenv("DB_DB") or "mssp"
    # DB_HOST = os.getenv("DB_HOST") or "192.168.69.194"
    # DB_PORT = os.getenv("DB_PORT") or "5005"

    # DB_DB = "mssp"
    # DB_HOST = "localhost"


    # REDIS_HOST = os.getenv("REDDIS_HOST") or "192.168.69.194"
    # REDIS_HOST = 'localhost'

    # SQLAlchemy
    # SQLALCHEMY_POOL_RECYCLE = 540
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = (
    #     f"mysql+pymysql://{DB_USER}:{DB_CODE}@{DB_HOST}:{DB_PORT}/{DB_DB}"
    # )

    # Log Path
    LOGGING_LOCATION = "./log/mssp/mssp-api.log"

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = 3000
    JWT_REFRESH_TOKEN_EXPIRES = 7200

    # Flask-APSchedule
    SCHEDULER_API_ENABLED = False

    # TWCERT Submit MAIL
    TWCERT_EMAIL = "raymond@billows.com.tw"




