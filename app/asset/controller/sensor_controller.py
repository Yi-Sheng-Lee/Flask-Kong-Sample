from flask import request
from flask_restful import Resource
from app.asset.service.sensor_service import (
    get_sensor_kv_list,
    delete_sensor,
    get_sensor_by_filter,
    update_sensor,
    add_sensor,
    get_sensor
)
from common.util.response_util import return_response
from app.auth.util.decorator import auth_required, error_handler
from flask_jwt_extended import jwt_required

from app.operator_record.service.operator_record_service import add_record_to_db


import logging

logger = logging.getLogger(__name__)


class Sensor(Resource):
    @classmethod
    @auth_required("/sensor/sensor-manage", "VIEW")
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the sensor")
            res = get_sensor(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            add_record_to_db(False, error=e.args[0])
            logger.error(e)

    @classmethod
    @auth_required("/sensor/sensor-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to create the sensor")
            payload = request.get_json()
            res = add_sensor(**payload)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/sensor/sensor-manage", "UPDATE")
    @error_handler
    def put(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to put the sensor")
            payload = request.get_json()
            res = update_sensor(uid, **payload)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])


class Sensors(Resource):
    @classmethod
    @auth_required("/sensor/sensor-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the sensor")
            payload = request.get_json()
            res = get_sensor_by_filter(**payload) if payload else get_sensor_by_filter()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/sensor/sensor-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to delete the sensor")
            payload = request.get_json()
            if not payload:
                add_record_to_db(True, action="DELETE")
                return return_response(True, [])
            res = delete_sensor(payload)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class SensorMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the sensor menu list by company id")
            cid = request.args.get('cid')
            type = request.args.get('type')
            res = get_sensor_kv_list(**request.args)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])
