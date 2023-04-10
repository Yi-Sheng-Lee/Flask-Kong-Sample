import json
import os
from datetime import datetime, timedelta
from flask import current_app
from marshmallow import INCLUDE
import redis
from flask_jwt_extended import get_jwt_claims
from app.asset.dao.company_dao import CompanyDao
from app.asset.dao.sensor_dao import SensorDao
from app.asset.dao.device_dao import DeviceDao
from app.asset.dao.device_group_dao import DeviceGroupDao
from app.auth.dao.user_dao import UserDao
# from app.data_migrate.service.lm_service import get_asset_list_from_lm
# from app.security_event.dao.incident_dao import IncidentDao
from common.enum.code_enum import ApiTokenType, SensorType
from common.enum.service_enum import ServiceError
from app.asset.model.models import Device
from app.asset.schema.schemas import DeviceStatusInfoSchema, DeviceSchema, DeviceFormSchema, SensorFormSchema

import logging
import csv
import codecs

from app.asset.service.avt_service import get_asset_info_from_avt, get_asset_list_from_avt, integrate_avt_asset_data

logger = logging.getLogger(__name__)


def add_device(**kwargs):
    """
    新增 Device
    :param kwargs:
    :return:
    """
    device_form_data = DeviceFormSchema(unknown=INCLUDE).load(kwargs)
    device_dao = DeviceDao()

    if not device_form_data["company_uid"]:
        claims = get_jwt_claims()
        company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company = CompanyDao().get_one_by_fields(uid=device_form_data["company_uid"])
        company_id = company.id

    if not company_id:
        logger.error(ServiceError.COMPANY_NOT_EXIST.value)
        raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

    group = None
    if "group_uid" in device_form_data.keys() and device_form_data["group_uid"]:
        group = DeviceGroupDao().get_one_by_fields(uid=device_form_data["group_uid"])
        if not group:
            logger.error(ServiceError.GROUP_NOT_EXIST.value)
            raise Exception(ServiceError.GROUP_NOT_EXIST.value)

    device = Device()
    device.name = device_form_data["name"]
    device.company_id = company_id
    device.hostname = device_form_data["hostname"]
    device.ip = device_form_data["ip"]
    device.description = device_form_data["description"]
    device.type = device_form_data["type"]
    device.os = device_form_data["os"]
    device.sensor_id = device_form_data["sensor_id"]
    device.asset_id = device_form_data["asset_id"]
    device.monitoring = device_form_data["monitoring"]
    device_dao.add(device)

    if device.id and "managers" in device_form_data.keys():
        # 新增管理者
        managers = []
        for user_uid in device_form_data["managers"]:
            user = UserDao().get_by_uid(user_uid)
            if user:
                managers.append(user)
        device.managers = managers
        device_dao.update(device)

    return DeviceSchema().dump(device)


def update_device(uid, **kwargs):
    """
    更新 device 資料 by uid
    :param uid:
    :param kwargs:
    :return:
    """
    device_form_data = DeviceFormSchema().load(kwargs)
    device_schema = DeviceSchema()
    device_dao = DeviceDao()
    device = device_dao.get_one_by_fields(uid=uid)

    if not device:
        raise Exception(ServiceError.DATA_NOT_FOUND.value)

    if not device_form_data["company_uid"]:
        claims = get_jwt_claims()
        new_company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company = CompanyDao().get_one_by_fields(uid=device_form_data["company_uid"])
        new_company_id = company.id if company else 0

    if not new_company_id:
        logger.error(ServiceError.COMPANY_NOT_EXIST.value)
        raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

    new_group = None
    if "group_uid" in device_form_data.keys() and device_form_data["group_uid"] and device.group.uid != \
            device_form_data["group_uid"]:
        new_group = DeviceGroupDao().get_one_by_fields(uid=device_form_data["group_uid"])
        if not new_group:
            logger.error(ServiceError.GROUP_NOT_EXIST.value)
            raise Exception(ServiceError.GROUP_NOT_EXIST.value)

    if new_group:
        device.group_id = new_group.id

    device.name = device_form_data["name"]
    device.hostname = device_form_data["hostname"]
    device.ip = device_form_data["ip"]
    device.description = device_form_data["description"]
    device.type = device_form_data["type"]
    device.os = device_form_data["os"]
    device.monitoring = device_form_data["monitoring"]
    # device.company_id = new_company_id

    # 更新管理者
    managers = []
    for user_uid in device_form_data["managers"]:
        user = UserDao().get_by_uid(user_uid)
        if user:
            managers.append(user)
    device.managers = managers
    device_dao.update(device)
    device_dao.commit()
    return device_schema.dump(device)


def delete_devices(uids):
    """
    刪除Device by uid
    :param uids:
    :return:
    """
    res = []
    for uid in uids:
        device = DeviceDao().get_one_by_fields(uid=uid)
        if device:
            DeviceDao().delete(device)
            res.append(uid)
    return res


def get_device(uid):
    """
    取得設備明細 by device uid
    :param uid:
    :return:
    """
    device_dao = DeviceDao()
    device = device_dao.get_one_by_fields(uid=uid)
    if not device:
        raise Exception(ServiceError.DATA_NOT_FOUND.value)
    schema = DeviceSchema(exclude=["company_id", "group_id", "sensor_id"])
    res = schema.dump(device)
    return res


def get_device_by_filter(**kwargs):
    """
    取得設備清單（可做欄位過濾）
    :param kwargs:
    :return:
    """
    device_dao = DeviceDao()
    device_dao.set_order_by(["company_id","id"])

    device_schema = DeviceSchema(exclude=["company_id", "group_id", "sensor_id"])
    if "page" in kwargs:
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 10)
        del kwargs["page"]
        del kwargs["per_page"]

        for k, v in kwargs.items():
            device_dao.set_filter_field_like(k, v)
        device_dao.set_pager(page, per_page)
        res = device_dao.get_all_by_fields(**kwargs)
        res["data"] = device_schema.dump(res["data"], many=True)
    else:
        for k, v in kwargs.items():
            device_dao.set_filter_field_like(k, v)
        devices = device_dao.get_all_by_fields(**kwargs)
        res = device_schema.dump(devices, many=True)

    return res


def get_region_group_devices(city_code):
    """
    取得設備群組清單 by city_code
    :param city_code:
    :return:
    """
    res = DeviceDao().get_sensor_device(city_code=city_code)
    redis_cli = redis.Redis(
        host=current_app.config['REDIS_HOST'],
        db=current_app.config['REDIS_AVT_DB'],
        password=current_app.config['REDIS_PWD'],
        decode_responses=True
    )
    result = []
    try:
        for dev in res:
            group = next((item for item in result if item["group_id"] == dev.group.id), None)
            dev_status_json = redis_cli.get(f"{dev.sensor_id}_{dev.asset_id}")
            dev_status = {}
            if dev_status_json:
                dev_status = json.loads(dev_status_json)
            dev_status_code = {
                'N/A': True,
                'UP': True,
                'DOWN': False
            }
            if not group:
                # 新Group群
                data = {
                    'group_id': dev.group.id,
                    'group_name': dev.group.name,
                    'devices': [
                        {
                            "asset_id": dev.asset_id,
                            "hostname": dev.hostname,
                            "ip": dev.ip.split(',')[0],
                            "connected": dev_status_code[dev_status["availabilities"][
                                "value"]] if "availabilities" in dev_status.keys() else False,
                            "alarms": dev_status['alarms']['value']
                        }
                    ]
                }
                result.append(data)
            else:
                group['devices'].append(
                    {
                        "asset_id": dev.asset_id,
                        "hostname": dev.hostname,
                        "ip": dev.ip.split(',')[0],
                        "connected": dev_status_code[
                            dev_status["availabilities"]["value"]] if "availabilities" in dev_status.keys() else False,
                        "alarms": dev_status['alarms']['value']
                    }
                )
    except Exception as e:
        logger.info(e)
    finally:
        redis_cli.close()
    return result


def get_device_details(uid):
    """
    從Sensor取得設備明細資料
    :param uid:
    :return:
    """
    # 從Sensor取得設備明細, 目前僅有AVT設備，未來需要增加從各種設備抓取資料, 目前已知有lm尚未處理
    # 20211021 Raymond 流程修改為由Sensor定期發送資料給MSSP令存在Redis內，此Method暫時無使用
    device = DeviceDao().get_one_by_fields(uid=uid)
    if not device:
        raise Exception('Device not found')

    device_info_factory = {
        SensorType.ALIENVAULT.value: get_asset_info_from_avt,
        SensorType.LOG_MASTER.value: get_asset_info_from_avt
    }

    try:
        device_info_fn = device_info_factory[device.sensor.type]
        device_info = device_info_fn(device.sensor.uid, device.sensor.ip, device.asset_id)

        res = DeviceStatusInfoSchema().dump(device)
        res = {**res, **device_info}

        return res
    except Exception as e:
        logger.error(e, exc_info=True)
        return None


def get_device_kv_list(**kwargs):
    """
    取得Device key value list
    :param kwargs:
    :return:
    """
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0

    # 確認不是 最上層的 Company
    if company_id > 1:
        kwargs["company_id"] = company_id
    device_dao = DeviceDao()
    device_dao.set_order_by(["company_id"])
    devices = device_dao.get_all_by_fields(**kwargs) if kwargs else device_dao.get_all_by_fields()
    res = [{"uid": device.uid, "name": device.name if device.name else device.hostname, "type": device.type,
            "ip": device.ip} for device in devices]
    return res


def get_device_list_from_sensor(sensor_uid):
    """
    抓取外部Sensor Device資料
    :param sensor_uid:
    :return:
    """
    func_factory = {
        ApiTokenType.ALIENVAULT.value: get_asset_list_from_avt,
        ApiTokenType.MINISOC.value: get_asset_list_from_avt,
        # ApiTokenType.LOG_MASTER.value: get_asset_list_from_lm
    }

    sensor = SensorDao().get_one_by_fields(uid=sensor_uid)
    if not sensor:
        raise Exception(ServiceError.SENSOR_NOT_EXIST.value)

    func = func_factory[sensor.type]
    return func(sensor.company.uid, sensor.uid)


def import_devices(payload):
    """
    批次匯入Devices

    :param payload:
    :return:
    """
    devices_form_data = DeviceFormSchema().load(payload, many=True)
    res = []
    for form_data in devices_form_data:
        # if not form_data["company_uid"]:
        #     claims = get_jwt_claims()
        #     company_id = claims["company_id"] if "company_id" in claims.keys() else 0
        #     company = CompanyDao().get_one_by_fields(id=company_id)
        # else:
        #     company = CompanyDao().get_one_by_fields(uid=form_data["company_uid"])

        # if not company:
        #     logger.error(ServiceError.COMPANY_NOT_EXIST.value)
        #     continue

        sensor = SensorDao().get_one_by_fields(uid=form_data['sensor_uid'])
        sensor_schema = SensorFormSchema().dump(sensor)
        company = CompanyDao().get_one_by_fields(uid=sensor_schema['company_uid'])
        if not sensor:
            logging.error(f"Import device failed, CODE: {ServiceError.SENSOR_NOT_EXIST} Data: {json.dumps(form_data)}")
            continue

        device = DeviceDao().get_one_by_fields(ip=form_data["ip"], sensor_uid=form_data["sensor_uid"])

        # get default group
        default_group = DeviceGroupDao().get_one_by_fields(company_id=company.id, is_default=1)

        try:
            if not device:
                logger.info(f"Company {company.id} import device: {form_data['ip']}")
                device = Device()

            device.name = form_data["name"]
            device.company_id = company.id
            device.hostname = form_data["hostname"]
            device.ip = form_data["ip"]
            device.description = form_data["description"]
            device.os = form_data["os"]
            device.type = form_data["type"]
            device.sensor_id = sensor.id
            device.asset_id = form_data["asset_id"]
            device.group_id = default_group.id

            if not device.id:
                DeviceDao().add(device)
            else:
                DeviceDao().update(device)
            res.append(DeviceSchema(exclude=["company_id", "group_id", "company"]).dump(device))
        except Exception as e:
            logging.error(f"Import device failed, Data: {json.dumps(form_data)}")
            continue

    return res


def import_devices_by_csv(req_file, sensor_uid):
    sensor = SensorDao().get_by_uid(sensor_uid)
    data = csv.DictReader(codecs.iterdecode(req_file, "utf-8-sig"), delimiter=";")
    devices_list = list(data)
    devices = []
    for device in devices_list:
        devices.append({
            "sensor_uid": sensor_uid,
            "sensor_name": sensor.name,
            "sensor_type": sensor.type,
            "sensor_ip": sensor.ip,
            "name": device["Hostname"],
            "hostname": device["Hostname"],
            "asset_id": device["Host ID"],
            "ip": device["IPs"],
            "type": "IT001",
            "os": device["Operating System"]
        })
    return sensor_device_insert_data_db(sensor_uid, devices)


def get_sensor_device_data(uid, monitoring=True, payload={}):
    filters = {
        "sensor_uid": uid
    }

    if monitoring:
        filters["monitoring"] = 1

    monitor_devices = DeviceDao().get_all_by_fields(**filters)
    device_groups = []
    for monitor_device in monitor_devices:
        group_id = monitor_device.group.id if monitor_device.group else 0
        group_uid = monitor_device.group.uid if monitor_device.group else 0
        group_name = monitor_device.group.name if monitor_device.group else "UNGROUPED"
        group_type = monitor_device.group.type if monitor_device.group else "IT"
        topology_img = monitor_device.group.topology_img if monitor_device.group and monitor_device.group.topology_img else ""
        group_sort = monitor_device.group.sort if monitor_device.group else 999
        has_topology = monitor_device.group.has_topology if monitor_device.group else 0
        # alarms_count = IncidentDao().get_device_incident_count(monitor_device.id)
        sensor_type = monitor_device.sensors.type

        group_data = next((group for group in device_groups if group["group_id"] == group_id), None)
        if not group_data:
            group_data = {
                'group_id': group_id,
                'group_uid': group_uid,
                'group_name': group_name,
                'group_type': group_type,
                'sort': group_sort,
                'topology_img': topology_img,
                'has_topology': has_topology,
                'devices': [
                    {
                        "uid": monitor_device.uid,
                        "asset_id": monitor_device.asset_id,
                        "hostname": monitor_device.hostname,
                        "ip": monitor_device.ip,
                        "type": monitor_device.type,
                        "lat": monitor_device.lat if monitor_device.lat else "",
                        "lng": monitor_device.lng if monitor_device.lng else "",
                        "connected": True,
                        # "alarms": alarms_count,
                        'sensor_type': sensor_type,
                    }
                ]
            }
            device_groups.append(group_data)
        else:
            group_data["devices"].append(
                {
                    "uid": monitor_device.uid,
                    "asset_id": monitor_device.asset_id,
                    "hostname": monitor_device.hostname,
                    "ip": monitor_device.ip,
                    "type": monitor_device.type,
                    "lat": monitor_device.lat if monitor_device.lat else "",
                    "lng": monitor_device.lng if monitor_device.lng else "",
                    "connected": True,
                    # "alarms": alarms_count,
                    'sensor_type': sensor_type,
                }
            )
    device_groups = sorted(device_groups, key=lambda item: item.get("sort"))
    return device_groups


def get_sensor_monitoring_devices(sensor_uid):
    """
    取得monitoring device data (簡易)
    :param sensor_uid:
    :return:
    """
    devices = DeviceDao().get_sensor_monitoring_devices(sensor_uid)
    res = DeviceSchema(many=True, only=["uid", "ip", "name", "asset_id"]).dump(devices)
    return res


def sensor_device_sync_data_factory(sensor_uid, devices_data):
    """
    OPEN API 使用，給外部Sensor丟回設備資料，另存成Json file
    File Format 為
    :param sensor_uid:
    :param payload:
    :return:
    """

    try:
        sensor = SensorDao().get_by_uid(sensor_uid)
        if not sensor:
            raise Exception(ServiceError.SENSOR_NOT_EXIST.value)

        sensor_device_dir_path = os.path.join(
            current_app.blueprints["asset"].static_folder,
            f"{current_app.config['SENSOR_TMP_FILE_PATH']}",
            sensor.company.uid,
        ) + "/"

        if not os.path.exists(os.path.dirname(sensor_device_dir_path)):
            logger.info(f"create sensor tmp device path: {sensor_device_dir_path}")
            os.makedirs(os.path.dirname(sensor_device_dir_path), exist_ok=True)

        tmp_filepath = os.path.join(sensor_device_dir_path, f"{sensor.uid}.json")

        with open(tmp_filepath, 'w') as tmp_file:
            tmp_file.write(json.dumps(devices_data))

        logger.info(f"Update company: {sensor.company.name}, sensor: {sensor.name} temp devices data")
        logger.info(f"Path: {tmp_filepath}")

    except Exception as e:
        logger.error(e, exc_info=True)
        return []


def sensor_device_insert_data_db(sensor_uid, devices_data):
    """
    OPEN API 使用，給外部Sensor丟回設備資料，判斷Ip是否存在，若不存在直接寫入資料庫
    File Format 為
    :param sensor_uid:
    :param payload:
    :return:
    """

    try:
        sensor = SensorDao().get_by_uid(sensor_uid)
        company_id = sensor.company_id
        default_group = DeviceGroupDao().get_one_by_fields(company_id=company_id, is_default=1)

        if not sensor:
            raise Exception(ServiceError.SENSOR_NOT_EXIST.value)
        if not company_id:
            raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

        for device_data in devices_data:
            # 判斷IP是否已存在
            device = DeviceDao().get_one_by_fields(ip=device_data["ip"], sensor_uid=sensor_uid, company_id=company_id)
            if not device:
                # 針對不存在的ip資料進行新增
                logger.info(f"Company {company_id} import device: {device_data['ip']}")
                device = Device()
                device.name = device_data["hostname"] if device_data["hostname"] else device_data['ip']
                device.company_id = company_id
                device.hostname = device_data["hostname"] if device_data["hostname"] else device_data['ip']
                device.ip = device_data["ip"]
                device.os = device_data["os"]
                device.type = device_data["type"]
                device.sensor_id = sensor.id
                device.asset_id = device_data["asset_id"]
                device.group_id = default_group.id
                device.description = ""
                DeviceDao().add(device)
            else:
                logger.info(f"{device_data['hostname']} is existed")

    except Exception as e:
        logger.error(e, exc_info=True)
    return []


def sensor_device_status_data_update(sensor_uid, devices_data):
    """
    OPEN API 同步 sensor上的資料到 MSSP Redis 內
    :param sensor_uid:
    :param devices_data:
    :return:
    """
    try:
        sensor = SensorDao().get_by_uid(sensor_uid)
        if not sensor:
            logger.error()
            raise Exception(ServiceError.SENSOR_NOT_EXIST.value)

        redis_cli = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            db=current_app.config['REDIS_AVT_DB'],
            password=current_app.config['REDIS_PWD'],
            decode_responses=True
        )

        for dev_uid, data in devices_data.items():
            device = DeviceDao().get_one_by_fields(uid=dev_uid, sensor_uid=sensor_uid)
            if not device:
                logger.error(f"Device {dev_uid} not found in sensor {sensor_uid}")
                continue

            logger.info(f"Update {dev_uid} status data from sensor {sensor_uid}")
            redis_cli.set(name=f"{sensor_uid}_{dev_uid}", value=json.dumps(data))
    except Exception as e:
        logger.error(e, exc_info=True)
        return None


def get_device_status_info(device_uid):
    """
    從Redis內取得Sensor發送過來的device status info data
    :param device_uid:
    :return:
    """
    try:
        device = DeviceDao().get_by_uid(device_uid)
        if not device:
            logger.error(f"Device Not found, uid: {device_uid} CODE:{ServiceError.DEVICE_NOT_EXIST.value}")
            raise Exception(ServiceError.DEVICE_NOT_EXIST.value)

        redis_cli = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            db=current_app.config['REDIS_AVT_DB'],
            password=current_app.config['REDIS_PWD'],
            decode_responses=True
        )

        res = redis_cli.get(f"{device.sensor_uid}_{device_uid}")
        if res:
            res = json.loads(res)
            if device.sensor.type == 'avt':
                res = integrate_avt_asset_data(res)
        else:
            res = {
                "alarms_list": [],
                "events_list": [],
                "services_list": [],
                "vulnerabilities_list": [],
                "alarms": {"value": 0, "level": 0},
                "availabilities": {"value": "N/A", "level": 0},
                "events": {"value": 0, "level": 0},
                "services": {"value": 0, "level": 0},
                "vulnerabilities": {"value": 0, "level": 0}
            }

        device_info = {
            'ip': device.ip,
            'hostname': device.hostname,
            'name': device.name,
            'description': device.description,
            'type': device.type,
            'os': device.os
        }

        res.update(device_info)
        return res

    except Exception as e:
        logger.error(e, exc_info=True)
        return None
