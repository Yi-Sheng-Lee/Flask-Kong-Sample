from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.asset.service.device_service import (
    add_device,
    update_device,
    delete_devices,
    get_device,
    get_device_by_filter,
    get_device_kv_list,
    get_device_list_from_sensor,
    import_devices,
    import_devices_by_csv,
    get_sensor_monitoring_devices,
    sensor_device_sync_data_factory,
    sensor_device_status_data_update,
    get_device_status_info,
    sensor_device_insert_data_db
)
from app.auth.util.decorator import auth_required, error_handler
from common.util.response_util import return_response
from app.operator_record.service.operator_record_service import add_record_to_db

import logging

logger = logging.getLogger(__name__)


class DeviceStatusInfo(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the DeviceStatusInfo")
            res = get_device_status_info(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e)
            add_record_to_db(False, error=e)
            return return_response(False, e)


class Device(Resource):
    @classmethod
    @auth_required("/device/device-manage", "VIEW")
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the device")
            res = get_device(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/device/device-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to create the device")
            payload = request.get_json()
            res = add_device(**payload)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/device/device-manage", "UPDATE")
    @error_handler
    def put(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to put the device")
            payload = request.get_json()
            res = update_device(uid, **payload)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])


class Devices(Resource):
    @classmethod
    @auth_required("/device/device-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the devices")
            payload = request.get_json()
            res = get_device_by_filter(**payload) if payload else get_device_by_filter()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/device/device-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to delete the device")
            payload = request.get_json()
            if not payload:
                add_record_to_db(True, action="DELETE")
                return return_response(True, [])
            res = delete_devices(payload)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class DeviceMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the device menu list by sensor id")
            filters = {}
            if request.args.get("cid"):
                filters["company_uid"] = request.args.get("cid")
            if request.args.get("sid"):
                filters["sensor_uid"] = request.args.get("sid")
            if request.args.get("gid"):
                if request.args.get("gid") == "0":
                    # 未加入設備群組設備清單
                    filters["group_id"] = "0"
                else:
                    # 設備群組清單
                    filters["group_uid"] = request.args.get("gid")
            res = get_device_kv_list(**filters)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(True, error=e.args[0])
            return return_response(False, e.args[0])


class ExternalSensorDevices(Resource):
    @classmethod
    @auth_required("/device/device-manage", "CREATE")
    @error_handler
    def get(cls, sensor_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the devices data from sensor")
            res = get_device_list_from_sensor(sensor_uid)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    # @jwt_required
    @error_handler
    def post(cls, sensor_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to receive devices data from sensor")
            payload = request.get_json()
            res = sensor_device_sync_data_factory(sensor_uid, payload)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            return return_response(False, e.args[0])
    

class ExternalSensorDevicesAdd(Resource):
    
    @classmethod
    # @jwt_required
    @error_handler
    def post(cls, sensor_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to receive devices data from sensor")
            payload = request.get_json()
            res = sensor_device_insert_data_db(sensor_uid, payload)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            return return_response(False, e.args[0])

class OpenApiMonitorDevices(Resource):
    @classmethod
    @error_handler
    def get(cls, sensor_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the monitor devices data from sensor")
            res = get_sensor_monitoring_devices(sensor_uid)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            return return_response(False, e.args[0])


class OpenApiMonitorDeviceStatus(Resource):
    @classmethod
    @error_handler
    def put(cls, sensor_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to update devices status data from sensor")
            payload = request.get_json()
            res = sensor_device_status_data_update(sensor_uid, payload)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            return return_response(False, e.args[0])


class DevicesImport(Resource):
    @classmethod
    @auth_required("/device/device-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to import the devices")
            payload = request.get_json()
            res = import_devices(payload)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])


class DeviceImportByCsv(Resource):
    @classmethod
    @auth_required("/device/device-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            req_form = dict(request.form)
            sensor_uid = req_form["sensor_uid"]
            req_file = request.files.get("file")
            logger.info(f"[Resource] <{cls.__name__}> starts to import the devices by csv")
            res = import_devices_by_csv(req_file, sensor_uid)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])
