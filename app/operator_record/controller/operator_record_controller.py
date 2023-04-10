from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.auth.util.decorator import error_handler
from common.util.response_util import return_response
from app.operator_record.service.operator_record_service import get_record_by_filter, add_record_to_db, get_record_csv
from app.auth.util.decorator import auth_required

import logging

logger = logging.getLogger(__name__)


class Records(Resource):
    @classmethod
    @auth_required("/record/operation-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the record list")
            payload = request.get_json()
            res = get_record_by_filter(**(payload or {}))
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])


class DownloadRecord(Resource):
    @classmethod
    @auth_required("/record/operation-manage", "DOWNLOAD")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to get record csv")
            payload = request.get_json()
            res = get_record_csv(**(payload or {}))
            add_record_to_db(True, action="DOWNLOAD")
            return res
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DOWNLOAD", error=e.args[0])
            return return_response(False, e.args[0])
