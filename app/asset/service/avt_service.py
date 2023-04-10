import json
import logging
import os

import redis
import requests
from flask import current_app
from datetime import datetime, timedelta

from app.asset.dao.sensor_dao import SensorDao
from common.enum.api_enum import AlienVaultApi
from common.enum.service_enum import ServiceError

logger = logging.getLogger(__name__)

va_f = False

def update_asset_info_to_redis(sensor_uid, asset_id):
    try:
        redis_key = f"{sensor_uid}_{asset_id}"

        asset_data = get_asset_info_from_avt(sensor_uid, asset_id)

        if asset_data:
            redis_cli = redis.Redis(
                host=current_app.config['REDIS_HOST'],
                db=current_app.config['REDIS_AVT_DB'],
                password=current_app.config['REDIS_PWD'],
                decode_responses=True
            )

            redis_cli.set(name=redis_key, value=asset_data)
    except Exception as e:
        logger.error(e, exc_info=True)


def get_asset_info_from_avt(sensor_uid, sensor_ip, asset_id):
    """
    從AVT/OSSIM拉設備資料
    :param sensor_uid:
    :param sensor_ip:
    :param asset_id:
    :return:
    """
    try:
        api_url = AlienVaultApi.ASSET_INFO.value
        api_url = api_url.format(url=sensor_ip, asset_id=asset_id)
        res = requests.get(api_url, verify=va_f)
        if res.status_code == 200:
            logger.info(f"Fetch AlienVault device list data from Sensor {sensor_uid}, IP: {sensor_ip}, ASSET_ID: {asset_id}.")
            asset_data = dict(sorted(res.json().items()))
            res = integrate_avt_asset_data(asset_data)
            return res
        else:
            return {}

    except Exception as e:
        logger.error(e, exc_info=True)
        return {}


def get_asset_list_from_avt(company_uid, sensor_uid):
    """
    從檔案，撈取Sensor device tmp data．
    :param company_uid:
    :param sensor_uid:
    :return:
    """
    try:
        sensor_device_tmp_file_path = os.path.join(
            current_app.blueprints["asset"].static_folder,
            f"{current_app.config['SENSOR_TMP_FILE_PATH']}",
            company_uid,
            f"{sensor_uid}.json"
        )
        if not os.path.isfile(sensor_device_tmp_file_path):
            raise Exception(ServiceError.DATA_NOT_FOUND.value)

        with open(sensor_device_tmp_file_path) as json_file:
            data = json.load(json_file)

        devices_data = []
        for device in data:
            devices_data.append({
                'name': device.get('hostname'),
                'hostname': device.get('hostname'),
                'asset_id': device.get('asset_id'),
                'ip': device.get('ip').split(',')[0].strip(),
                'os': device.get('os') if device.get('os') else '',
                'sensor_uid': sensor_uid,
                'type': 'IT001'
            })
        return devices_data

    except Exception as e:
        logger.error(e, exc_info=True)
        return []


def integrate_avt_asset_data(asset_data):
    """
    整理AVT回來的asset資料
    :param asset_data:
    :return:
    """
    service_list = [
        {
            "ip_addr": item["1"],
            "port": item["2"],
            "protocol": item["3"],
            "name": item["4"],
        }
        for item in asset_data['services_list']
    ]
    event_list = [
        {
            "date": (datetime.strptime(item["0"], "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M:%S"),
            "signature": item["1"],
            "source": item["2"],
            "destination": item["3"],
            "sensor": item["4"],
            "risk": item["5"],
        }
        for item in asset_data['event_detail']
    ]
    vulnerabilities_list = [
        {
            "scan_time": (datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M:%S"),
            "asset": item[1],
            "vulnerabilities": item[2],
            "vuln_id": item[3],
            "service": item[4],
            "severity": item[5],
        }
        for item in asset_data['vulnerabilities_detail']
    ]
    alarm_list = [
        {
            "date": (datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M:%S"),
            "status": item["status"],
            "intent_strategy": item["ik"],
            "method": item["sc"],
            "risk": item["risk"],
            "otx": item["otx"],
            "source": item["src"],
            "destination": item["dst"],
        }
        for item in asset_data['alarm_detail']
    ]

    res = {
        "alarms_list": alarm_list,
        "events_list": event_list,
        "services_list": service_list,
        "vulnerabilities_list": vulnerabilities_list,
        "alarms": {
            "value": asset_data["alarms"]["value"],
            "level": asset_data["alarms"]["level"]
        },
        "availabilities": {
            "value": asset_data["availabilities"]["value"],
            "level": asset_data["availabilities"]["level"]
        },
        "events": {
            "value": asset_data["events"]["value"],
            "level": asset_data["events"]["level"]
        },
        "services": {
            "value": asset_data["services"]["value"],
            "level": asset_data["services"]["level"]
        },
        "vulnerabilities": {
            "value": asset_data["vulnerabilities"]["value"],
            "level": asset_data["vulnerabilities"]["level"]
        }
    }
    return res

