from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.asset.service.device_group_service import (
    get_device_group,
    add_device_group,
    update_device_group,
    get_device_group_by_filter,
    delete_device_group,
    get_device_group_kv_list
)
from app.auth.util.decorator import error_handler, auth_required
from common.util.response_util import return_response
from app.operator_record.service.operator_record_service import add_record_to_db

import logging

logger = logging.getLogger(__name__)


class DeviceGroup(Resource):
    @classmethod
    @auth_required("/device/device-group-manage", "VIEW")
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the device group")
            res = get_device_group(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            add_record_to_db(False, error=e)
            logger.error(e)

    @classmethod
    @auth_required("/device/device-group-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to create the device group")
            payload = request.get_json()
            res = add_device_group(**payload)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/device/device-group-manage", "UPDATE")
    @error_handler
    def put(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to put the device group")
            payload = request.get_json()
            res = update_device_group(uid, **payload)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])


class DeviceGroups(Resource):
    @classmethod
    @auth_required("/device/device-group-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the device group")
            payload = request.get_json()
            res = get_device_group_by_filter(**payload) if payload else get_device_group_by_filter()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/device/device-group-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to delete the device group")
            payload = request.get_json()
            if not payload:
                add_record_to_db(True, action="DELETE")
                return return_response(True, [])
            res = delete_device_group(payload)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class DeviceGroupMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the device group menu list")
            filters = {}
            if request.args.get("cid"):
                filters["company_uid"] = request.args.get("cid")
            if request.args.get("sid"):
                filters["sensor_uid"] = request.args.get("sid")
            if request.args.get("did"):
                filters["device_uid"] = request.args.get("did")
            res = get_device_group_kv_list(**filters)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])
