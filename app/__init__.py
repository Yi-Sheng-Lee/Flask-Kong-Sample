# from app.enum.code_enum import ConfigGroupCode
# from app.enum.controller_error_enum import ControllerErrorEnum
from common.enum.code_enum import ConfigGroupCode
from common.util.response_util import return_response
from flask import Flask, request

from common.enum.http_code_enum import HttpCodeEnum
from config.config_util import ConfigUtils
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy, DefaultMeta
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_wkhtmltopdf import Wkhtmltopdf
from flask_apscheduler import APScheduler
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
import importlib
import logging
import inspect
import os

# 針對migrate相關constraints，做upgrade/downgrade mapping的命名規則處理
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
wkhtmltopdf = Wkhtmltopdf()
scheduler = APScheduler()


def create_app():
    config_util = ConfigUtils()
    app = Flask(__name__,
                template_folder='templates',
                static_folder="static",
                static_url_path='/static'
                )
    app.config.from_object(config_util.config)

    def json_error(status_code):
        return "{'error_code': %s}" % status_code, status_code

    @app.errorhandler(404)
    def endpoint_not_found(error):
        app.logger.error("Endpoint not found: %s", request.path)
        return return_response(False, HttpCodeEnum.ENDPOINT_NOT_FOUND.value)

    @app.errorhandler(405)
    def method_not_allowed(error):
        app.logger.error("Method not allowed: %s", error)
        return return_response(False, HttpCodeEnum.METHOD_NOT_ALLOWED.value)

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error("Server Error: %s", error)
        return return_response(False, HttpCodeEnum.INTERNAL_SERVER_ERROR.value)

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error("Unhandled Exception: %s", e)
        return json_error(500)

    # Logging setup
    _log_level = logging.DEBUG if app.config["DEBUG"] else logging.INFO

    # Logging rotate handle
    log_path = app.config["LOGGING_LOCATION"]

    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logfile_handler = RotatingFileHandler(
        log_path,
        maxBytes=30 * 1024 * 1024,
        backupCount=5,
        encoding="UTF-8",
    )

    # Logging format handle
    logging_format = logging.Formatter(
        app.config["LOGGING_FORMAT"], datefmt="%Y-%m-%d %H:%M:%S"
    )
    logfile_handler.setFormatter(logging_format)
    app.logger.addHandler(logfile_handler)
    app.logger.setLevel(_log_level)

    # JWT
    jwt.init_app(app)

    # DB model
    db.init_app(app)

    # Marshmallow
    ma.init_app(app)

    # 若要執行db.create_all()，須在app.app_context()內實作
    with app.app_context():
        # 由flask-migrate管控之models必須在此import
        curr_path = os.path.dirname(os.path.abspath(__file__))
        # 自動匯入 app module 下的 model
        # 此部分會因為載入順序問題，目前先寫死
        # "system", "download", "mail", "security_event", "report", "regulation",
        # "data_migrate", "dashboard", "stix_information"
        for app_dir in ["asset", "auth", "operator_record"]:
            app_model = os.path.join(curr_path, app_dir, 'model', 'models.py')
            if os.path.isfile(app_model):
                package_path = '.'.join(['app', app_dir, 'model', 'models'])
                logging.info(f'import package path: {package_path}')
                models = [model for model in inspect.getmembers(importlib.import_module(package_path), inspect.isclass) if type(model[1]) == DefaultMeta]
                for model in models:
                    model_path = '.'.join(['app', app_dir, 'model', 'models', ])
                    logging.info(f"Flask init model: {model_path}")
                    __import__(package_path, fromlist=[model[0]])

        migrate.init_app(app, db)

    # flask_wkhtmltopdf
    wkhtmltopdf.__init__(app)

    # APSchedule
    # if config_util.config.SCHEDULER_API_ENABLED:
    #     if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #         with app.app_context():
    #             from app.system.service.config_service import get_group_config
    #             notify_config = get_group_config(ConfigGroupCode.NOTIFICATION_INCIDENT.value)
    #             jobs = app.config["JOBS"]
    #             job = next((job for job in jobs if job["id"] == "IncidentTodoNotification"), None)
    #             job['minutes'] = int(notify_config["interval"]) if notify_config else 1440
    #             app.config["JOBS"] = jobs
    #         scheduler.init_app(app)
    #         scheduler.start()

    # CROS
    CORS(app)

    return app
