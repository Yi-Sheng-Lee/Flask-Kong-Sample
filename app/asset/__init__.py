from flask import Blueprint
from flask_restful import Api
from app.asset.controller.company_controller import Company, Companies, CompanyMenu, CompanyActive
from app.asset.controller.sensor_controller import SensorMenu, Sensors, Sensor
from app.asset.controller.device_group_controller import DeviceGroup, DeviceGroups, DeviceGroupMenu
from app.asset.controller.device_controller import (
    Device,
    Devices,
    DeviceMenu,
    DevicesImport,
    DeviceImportByCsv,
    ExternalSensorDevices,
    DeviceStatusInfo, OpenApiMonitorDevices, OpenApiMonitorDeviceStatus,ExternalSensorDevicesAdd
)


def create_module():
    bp = Blueprint('asset', __name__, static_folder="static")
    api = Api(bp)

    # Company
    api.add_resource(Company, "/api/1.0/company", "/api/1.0/company/<string:uid>")
    api.add_resource(Companies, "/api/1.0/companies")
    api.add_resource(CompanyMenu, "/api/1.0/company/menu")
    api.add_resource(CompanyActive, "/api/1.0/companies/active")

    # Sensor
    api.add_resource(Sensor, "/api/1.0/sensor", "/api/1.0/sensor/<string:uid>")
    api.add_resource(Sensors, "/api/1.0/sensors")
    api.add_resource(SensorMenu, "/api/1.0/sensor/menu")

    # Device Group
    api.add_resource(DeviceGroup, "/api/1.0/device-group", "/api/1.0/device-group/<string:uid>")
    api.add_resource(DeviceGroups, "/api/1.0/device-groups")
    api.add_resource(DeviceGroupMenu, "/api/1.0/device-group/menu")

    # Device
    api.add_resource(Device, "/api/1.0/device", "/api/1.0/device/<string:uid>")
    api.add_resource(Devices, "/api/1.0/devices")
    api.add_resource(DeviceMenu, "/api/1.0/device/menu")
    api.add_resource(ExternalSensorDevices, "/api/1.0/devices/sync/<string:sensor_uid>")
    api.add_resource(ExternalSensorDevicesAdd, "/api/1.0/devices/insert/<string:sensor_uid>")
    api.add_resource(DevicesImport, "/api/1.0/devices/import")
    api.add_resource(DeviceImportByCsv, "/api/1.0/devices/import/csv")
    api.add_resource(OpenApiMonitorDevices, "/api/1.0/devices/monitoring/<string:sensor_uid>")
    api.add_resource(OpenApiMonitorDeviceStatus, "/api/1.0/devices/monitoring/status/<string:sensor_uid>")
    return bp
