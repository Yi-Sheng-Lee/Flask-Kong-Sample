from flask import Blueprint
from flask_restful import Api

from app.operator_record.controller.operator_record_controller import Records, DownloadRecord
from app.operator_record.controller.web_url_controller import WebUrlMenu


def create_module():
    bp = Blueprint("operator_record", __name__)
    api = Api(bp)
    api.add_resource(Records, "/api/1.0/records")
    api.add_resource(DownloadRecord, "/api/1.0/record/download")
    api.add_resource(WebUrlMenu, "/api/1.0/web-url/menu")
    return bp
