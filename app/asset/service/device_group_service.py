import json
from flask import current_app
import logging
from datetime import date, datetime, timedelta
import logging

from flask_jwt_extended import get_jwt_claims
from marshmallow import INCLUDE

from app.asset.dao.company_dao import CompanyDao
from app.asset.dao.device_dao import DeviceDao
from app.asset.dao.device_group_dao import DeviceGroupDao
from app.asset.dao.device_group_topology_dao import DeviceGroupTopologyDao
from app.asset.dao.sensor_dao import SensorDao
from common.enum.service_enum import ServiceError
from app.asset.model.models import DeviceGroup, DeviceGroupTopology
from app.asset.schema.schemas import DeviceGroupSchema, DeviceGroupFormSchema

logger = logging.getLogger(__name__)


def get_device_group(uid):
    group = DeviceGroupDao().get_one_by_fields(uid=uid)
    return DeviceGroupSchema(exclude=["company_id"]).dump(group)


def get_device_group_kv_list(**kwargs):
    if "device_uid" in kwargs.keys():
        device = DeviceDao().get_by_uid(kwargs["device_uid"])
        kwargs["company_id"] = device.company_id
    elif "company_uid" not in kwargs.keys():
        claims = get_jwt_claims()
        if claims["company_id"] != 1:
            kwargs["company_id"] = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company = CompanyDao().get_by_uid(kwargs["company_uid"])
        if not company:
            logger.error(ServiceError.COMPANY_NOT_EXIST.value)
            raise Exception(ServiceError.COMPANY_NOT_EXIST.value)
        kwargs["company_id"] = company.id

    device_group_dao = DeviceGroupDao()
    device_group_dao.set_order_by(["company_id"])
    groups = device_group_dao.get_all_by_fields(**kwargs)
    if "sensor_uid" in kwargs.keys():
        tmp_groups = []
        for group in groups:
            for sensor in group.company.sensors:
                if sensor.uid == kwargs["sensor_uid"]:
                    if group not in tmp_groups:
                        tmp_groups.append(group)

        groups = tmp_groups

    res = [{"uid": group.uid, "name": group.name, "company_name": group.company.name} for group in groups]
    return res


def get_device_group_by_filter(**kwargs):
    device_group_dao = DeviceGroupDao()

    device_group_dao.set_order_by(["company_id"])
    schema = DeviceGroupSchema(exclude=["company_id"])

    if "page" in kwargs:
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 10)
        del kwargs["page"]
        del kwargs["per_page"]

        for k, v in kwargs.items():
            device_group_dao.set_filter_field_like(k, v)
        device_group_dao.set_pager(page, per_page)

        res = device_group_dao.get_all_by_fields()
        res["data"] = schema.dump(res["data"], many=True)
    else:
        for k, v in kwargs.items():
            device_group_dao.set_filter_field_like(k, v)

        groups = device_group_dao.get_all_by_fields()
        res = schema.dump(groups, many=True)

    return res


def add_device_group(**kwargs):
    form_data = DeviceGroupFormSchema().load(kwargs)
    device_group_dao = DeviceGroupDao()

    if not form_data["company_uid"]:
        claims = get_jwt_claims()
        company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company = CompanyDao().get_one_by_fields(uid=form_data["company_uid"])
        company_id = company.id if company else 0

    if not company_id:
        logger.error(ServiceError.COMPANY_NOT_EXIST.value)
        raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

    device_group = DeviceGroup()
    device_group.company_id = company_id
    device_group.name = form_data.get('name')
    device_group.type = form_data.get('type')
    device_group.sort = form_data.get('sort', '1')
    device_group.description = form_data.get('description')
    device_group.is_default = form_data.get('is_default')
    device_group.topology_img = form_data.get('topology_img')
    device_group.has_topology = form_data.get('has_topology')
    device_group_dao.add(device_group)

    if not device_group.id:
        raise Exception(ServiceError.CREATE_ERROR.value)

    form_devices = [dev['uid'] for dev in form_data.get('devices')]
    device_dao = DeviceDao()
    res = device_dao.update_devices_group(form_devices, device_group.id)

    dev_group_topology_dao = DeviceGroupTopologyDao()
    for device_topology in form_data.get('devices'):
        device = DeviceDao().get_one_by_fields(uid=device_topology.get('uid'))
        if device:
            topology = DeviceGroupTopology() if not device.topology else device.topology
            topology.group_id = device_group.id
            topology.device_id = device.id
            topology.lat = device_topology.get('lat', '')
            topology.lng = device_topology.get('lng', '')
            if not topology.id:
                dev_group_topology_dao.add(topology)
            else:
                dev_group_topology_dao.update(topology)

    return DeviceGroupSchema(exclude=["company_id"]).dump(device_group)


def update_device_group(uid, **kwargs):
    form_data = DeviceGroupFormSchema(unknown=INCLUDE).load(kwargs)
    device_group_dao = DeviceGroupDao()

    device_group = device_group_dao.get_one_by_fields(uid=uid)
    if not device_group:
        logger.error(f"[{ServiceError.DATA_NOT_FOUND.value}] Device group not found, uid: {uid}")
        raise Exception(ServiceError.DATA_NOT_FOUND.value)

    if not form_data["company_uid"]:
        claims = get_jwt_claims()
        company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company = CompanyDao().get_one_by_fields(uid=form_data["company_uid"])
        company_id = company.id if company else 0

    if not company_id:
        logger.error(ServiceError.COMPANY_NOT_EXIST.value)
        raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

    # device_group.company_id = company_id
    device_group.name = form_data.get('name')
    device_group.type = form_data.get('type')
    device_group.sort = form_data.get('sort', '1')
    device_group.is_default = form_data.get('is_default')
    device_group.description = form_data.get('description')
    device_group.topology_img = form_data.get('topology_img')
    device_group.has_topology = form_data.get('has_topology')
    device_group_dao.update(device_group)

    # Get remove group devices
    curr_devices = [device.uid for device in device_group.devices]
    form_devices = [dev['uid'] for dev in form_data.get('devices')]
    delete_devices = list(set(curr_devices).difference(set(form_devices)))
    DeviceDao().update_devices_group(delete_devices, 0)

    # update device group_id
    DeviceDao().update_devices_group(form_devices, device_group.id)

    dev_group_topology_dao = DeviceGroupTopologyDao()
    for device_topology in form_data.get('devices'):
        device = DeviceDao().get_one_by_fields(uid=device_topology.get('uid'))
        if device:
            topology = DeviceGroupTopology() if not device.topology else device.topology
            topology.group_id = device_group.id
            topology.device_id = device.id
            topology.lat = device_topology.get('lat', '')
            topology.lng = device_topology.get('lng', '')
            if not topology.id:
                dev_group_topology_dao.add(topology)
            else:
                dev_group_topology_dao.update(topology)

    return DeviceGroupSchema(exclude=["company_id"]).dump(device_group_dao.get_by_id(device_group.id))


def delete_device_group(uids):
    device_group_dao = DeviceGroupDao()
    res = []
    for uid in uids:
        device_group = device_group_dao.get_one_by_fields(uid=uid)
        if not device_group:
            logger.error(f"[{ServiceError.DATA_NOT_FOUND.value}] Device group not found, uid: {uid}")
            continue

        # reset device group as default group
        default_group = DeviceGroupDao().get_one_by_fields(company_id=device_group.company_id, is_default=1)

        reset_device_uids = [device.uid for device in device_group.devices]
        if reset_device_uids:
            dev_dao = DeviceDao()
            dev_dao.update_devices_group(reset_device_uids, default_group.id)
        for topology in device_group.device_topology:
            device_group_dao.delete(topology)
        device_group_dao.delete(device_group)
        res.append(uid)
    return res
