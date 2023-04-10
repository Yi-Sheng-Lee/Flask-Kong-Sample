import logging
from marshmallow import INCLUDE
from app.asset.dao.company_dao import CompanyDao
from app.asset.dao.device_dao import DeviceDao
from app.asset.dao.sensor_dao import SensorDao
from common.enum.service_enum import ServiceError
from app.asset.model.models import Sensor
from app.asset.schema.schemas import SensorSchema, SensorFormSchema

logger = logging.getLogger(__name__)


def get_sensor(uid):
    sensor = SensorDao().get_one_by_fields(uid=uid)
    return SensorSchema(exclude=["company_id"]).dump(sensor)


def get_sensor_kv_list(**kwargs):
    sensors = SensorDao().get_all_by_fields(**kwargs)
    res = [{"uid": sensor.uid, "name": sensor.name, "company_name": sensor.company_name} for sensor in sensors]
    return res


def get_sensor_by_filter(**kwargs):
    try:
        sensor_dao = SensorDao()
        sensor_dao.set_order_by(["company_id"])

        schema = SensorSchema(exclude=["company_id"])

        if "page" in kwargs:
            page = kwargs.get("page", 1)
            per_page = kwargs.get("per_page", 10)

            del kwargs["page"]
            del kwargs["per_page"]

            for k, v in kwargs.items():
                sensor_dao.set_filter_field_like(k, v)
            sensor_dao.set_pager(page, per_page)
            res = sensor_dao.get_all_by_fields()
            res["data"] = schema.dump(res["data"], many=True)
        else:
            for k, v in kwargs.items():
                sensor_dao.set_filter_field_like(k, v)
            sensors = sensor_dao.get_all_by_fields()
            res = schema.dump(sensors, many=True)

    except Exception as e:
        logger.error(e)
    else:
        return res

    # sensors = sensor_dao.get_all_by_fields()
    # schema = SensorSchema(exclude=["company_id"])
    # res = schema.dump(sensors, many=True)
    # return res


def add_sensor(**kwargs):
    sensor_form_data = SensorFormSchema(unknown=INCLUDE).load(kwargs)
    sensor_dao = SensorDao()

    company = CompanyDao().get_one_by_fields(uid=sensor_form_data.get('company_uid'))
    if not company:
        logger.error(f'Create sensor failed CODE: {ServiceError.COMPANY_NOT_EXIST.value}')
        raise Exception(ServiceError.COMPANY_NOT_EXIST.value)

    # check name exist in sensor
    if sensor_dao.get_all_by_fields(company_uid=sensor_form_data.get('company_uid'), name=sensor_form_data.get('name')):
        logger.error(f'Create sensor failed CODE: {ServiceError.NAME_DUPLICATE.value}')
        raise Exception(ServiceError.NAME_DUPLICATE.value)

    # check ip exist
    if SensorDao().get_one_by_fields(ip=sensor_form_data.get("ip")):
        logger.error(f'Update sensor failed CODE: {ServiceError.SENSOR_IP_DUPLICATE.value}')
        raise Exception(ServiceError.SENSOR_IP_DUPLICATE.value)

    sensor_model = Sensor()
    sensor_model.ip = sensor_form_data.get('ip')
    sensor_model.type = sensor_form_data.get('type')
    sensor_model.name = sensor_form_data.get('name')
    sensor_model.description = sensor_form_data.get('description')
    sensor_model.company_id = company.id
    sensor_model.country_code = sensor_form_data.get('country_code')
    sensor_model.city_code = sensor_form_data.get('city_code')
    sensor_model.zip_code = sensor_form_data.get('zip_code')
    sensor_model.address = sensor_form_data.get('address')
    sensor_dao.add(sensor_model)
    return SensorSchema(exclude=["company_id"]).dump(sensor_model)


def update_sensor(uid, **kwargs):
    sensor_form_data = SensorFormSchema(unknown=INCLUDE).load(kwargs)
    sensor_dao = SensorDao()
    sensor = sensor_dao.get_one_by_fields(uid=uid)

    if not sensor:
        logger.error(f'Update sensor failed CODE: {ServiceError.DATA_NOT_FOUND.value}')
        raise Exception(ServiceError.DATA_NOT_FOUND.value)

    # check name exist in sensor
    if sensor_dao.get_all_without_uid(uid, company_uid=sensor_form_data.get('company_uid'), name=sensor_form_data.get('name')):
        logger.error(f'Update sensor failed CODE: {ServiceError.NAME_DUPLICATE.value}')
        raise Exception(ServiceError.NAME_DUPLICATE.value)

    if sensor.company_uid != sensor_form_data.get("company_uid"):
        company = CompanyDao().get_one_by_fields(uid=sensor_form_data.get('company_uid'))
        if not company:
            logger.error(f'Update sensor failed CODE: {ServiceError.COMPANY_NOT_EXIST.value}')
            raise Exception(ServiceError.COMPANY_NOT_EXIST.value)
        sensor.company_id = company.id

    if sensor.ip != sensor_form_data.get("ip"):
        exist_sensor = SensorDao().get_all_without_uid(uid=sensor.uid, ip=sensor_form_data.get("ip"))
        if exist_sensor:
            logger.error(f'Update sensor failed CODE: {ServiceError.SENSOR_IP_DUPLICATE.value}')
            raise Exception(ServiceError.SENSOR_IP_DUPLICATE.value)
        sensor.ip = sensor_form_data.get('ip')

    sensor.type = sensor_form_data.get('type')
    sensor.name = sensor_form_data.get('name')
    sensor.description = sensor_form_data.get('description')
    sensor.country_code = sensor_form_data.get('country_code')
    sensor.city_code = sensor_form_data.get('city_code')
    sensor.zip_code = sensor_form_data.get('zip_code')
    sensor.address = sensor_form_data.get('address')

    sensor_dao.update(sensor)

    # 更新Sensor 下的device 地區資訊
    # 20210823 Raymond 已修改為以Sensor位址為主
    # DeviceDao().update_device_sensor_area(sensor.id, sensor.country_code, sensor.city_code, sensor.zip_code)

    # Device 加入Sensor
    # sensor_devices = sensor_form_data.get("devices")
    # curr_sensor_devices = [device.uid for device in DeviceDao().get_all_by_fields(sensor_id=sensor.id)]
    # remove_devices = list(set(sensor_devices).symmetric_difference(set(curr_sensor_devices)))
    # for device_uid in sensor_devices:
    #     device = DeviceDao().get_one_by_fields(uid=device_uid)
    #     if not device:
    #         logger.error(f'Assign device failed CODE: {ServiceError.DEVICE_NOT_EXIST.value}')
    #         continue
    #
    #     device.sensor_id = sensor.id
    #     DeviceDao().update(device)

    return SensorSchema(exclude=["company_id"]).dump(sensor)


def delete_sensor(uids):
    res = []
    failed = []
    for uid in uids:
        sensor = SensorDao().get_one_by_fields(uid=uid)
        if sensor:
            if not sensor.devices:
                SensorDao().delete(sensor)
                res.append(uid)
            else:
                logger.error(f'Sensor devices is not empty. uid: {uid}')
                failed.append(uid)
    return res
