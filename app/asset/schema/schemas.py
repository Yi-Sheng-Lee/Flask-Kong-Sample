from app import ma
from ..model import models
from marshmallow import validate, validates

from ...auth.schema.schemas import UserSchema


class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Company
        load_instance = True
        include_fk = True
        exclude = ("create_at", "update_at")


class CompanyInputFormSchema(ma.Schema):
    class AdminUserSchema(ma.Schema):
        name = ma.Str(required=True)
        password = ma.Str(required=True)
        email = ma.Str(required=True)
        phone = ma.Str(required=True)

    name = ma.Str(required=True)
    contact = ma.Str(required=True)
    contact_tel = ma.Str()
    contact_email = ma.Str()
    country_code = ma.Str(required=True)
    city_code = ma.Str(required=True)
    zip_code = ma.Str(required=True)
    address = ma.Str()
    tax_id = ma.Str(required=True)
    description = ma.Str()
    admin_user = ma.Nested(AdminUserSchema)


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class DeviceSchema(ma.Schema):
        uid = ma.Str()
        name = ma.Str()
        hostname = ma.Str()
        ip = ma.Str()
        type = ma.Str()

    class Meta:
        model = models.Sensor
        load_instance = True
        include_fk = True
        exclude = ("create_at", "update_at", "create_user", "update_user", "id")

    company = ma.Nested(CompanySchema)
    devices = ma.Nested(DeviceSchema, many=True)


class SensorFormSchema(ma.Schema):
    name = ma.Str(required=True, validate=[validate.Length(min=1)])
    description = ma.Str()
    company_uid = ma.Str(required=True)
    ip = ma.Str(required=True)
    type = ma.Str(required=True)
    country_code = ma.Str(required=True)
    city_code = ma.Str(required=True)
    zip_code = ma.Str(required=True)
    address = ma.Str()
    devices = ma.List(ma.Str())


class DeviceGroupTopologySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.DeviceGroupTopology
        load_instance = True
        include_fk = True
        exclude = (
            "id",
            "device_id",
            "create_at",
            "create_user",
            "update_at",
            "update_user",
        )


class DeviceGroupSchema(ma.SQLAlchemyAutoSchema):
    class DeviceSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = models.Device
            load_instance = True
            include_fk = True
            exclude = (
                "id",
            )

        create_at = ma.DateTime("%Y-%m-%d %H:%M:%S")
        update_at = ma.DateTime("%Y-%m-%d %H:%M:%S")
        lat = ma.Str(default="", missing="")
        lng = ma.Str(default="", missing="")

    class Meta:
        model = models.DeviceGroup
        load_instance = True
        include_fk = True
        exclude = (
            "id",
            "create_at",
            "create_user",
            "update_at",
            "update_user",
        )

    company = ma.Nested(CompanySchema, only=("uid", "name"))
    devices = ma.Nested(DeviceSchema, many=True, only=("uid", "name", "hostname", "ip", "type", "description", "lat", "lng"))
    topology = ma.Nested(DeviceGroupTopologySchema)


class DeviceGroupFormSchema(ma.Schema):
    class DeviceSchema(ma.Schema):
        uid = ma.Str(required=True)
        lat = ma.Str()
        lng = ma.Str()

    company_uid = ma.Str(default="", missing="")
    devices = ma.Nested(DeviceSchema, many=True)
    name = ma.Str(required=True)
    type = ma.Str(required=True)
    has_topology = ma.Int(required=True)
    sort = ma.Int()
    description = ma.Str()
    topology_img = ma.Str()


class DeviceStatusInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Device
        load_instance = True
        exclude = (
            "id",
        )

        alarms = ma.Dict(keys=ma.Str(), values=ma.Str())
        alarm_list = ma.List(ma.Dict(keys=ma.Str(), values=ma.Str()))
        availabilities = ma.Dict(keys=ma.Str(), values=ma.Str())
        events = ma.Dict(keys=ma.Str(), values=ma.Str())
        event_list = ma.List(ma.Dict(keys=ma.Str(), values=ma.Str()))
        services = ma.Dict(keys=ma.Str(), values=ma.Str())
        services_list = ma.List(ma.Dict(keys=ma.Str(), values=ma.Str()))
        vulnerabilities = ma.Dict(keys=ma.Str(), values=ma.Str())
        vulnerabilities_list = ma.List(ma.Dict(keys=ma.Str(), values=ma.Str()))


class DeviceFormFieldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Device
        load_instance = True
        include_fk = True
        exclude = (
            "id",
            "create_at",
            "update_at",
        )
    company_id = ma.Int(required=True)
    sensor_id = ma.Int(required=True)
    group_id = ma.Int(required=True)
    name = ma.Str(required=True, validate=[validate.Length(min=1)])
    ip = ma.Str(required=True, validate=[validate.Length(min=1)])
    company = ma.Nested(CompanySchema(only=["uid", "pid", "name", "description"]))
    group = ma.Nested(DeviceGroupSchema(only=["uid", "name", "description", "description"]))
    topology = ma.Nested(DeviceGroupTopologySchema(exclude=["group_id"]))
    # managers = ma.List(ma.Str())


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Device
        load_instance = True
        include_fk = True
        exclude = (
            "id",
            "create_at",
            "update_at",
        )
    company_id = ma.Int(required=True)
    sensor_id = ma.Int(required=True)
    group_id = ma.Int(required=True)
    name = ma.Str(required=True, validate=[validate.Length(min=1)])
    ip = ma.Str(required=True, validate=[validate.Length(min=1)])
    company = ma.Nested(CompanySchema(only=["id", "uid", "pid", "name", "description"]))
    sensor = ma.Nested(SensorSchema(exclude=["company", "devices"]))
    group = ma.Nested(DeviceGroupSchema(only=["uid", "name", "description", "description"]))
    topology = ma.Nested(DeviceGroupTopologySchema(exclude=["group_id"]))
    managers = ma.Nested(UserSchema(only=["uid", "name", "email"]), many=True)


class DeviceFormSchema(ma.Schema):
    name = ma.Str(required=True, validate=[validate.Length(min=1)])
    hostname = ma.Str(required=True, validate=[validate.Length(min=1)])
    ip = ma.Str(required=True, validate=[validate.Length(min=1)])
    type = ma.Str(required=True, validate=[validate.Length(min=1)])
    sensor_uid = ma.Str(required=True, validate=[validate.Length(min=1)])
    os = ma.Str(default="", missing="")
    company_uid = ma.Str(default="", missing="")
    group_uid = ma.Str(default="", missing="")
    managers = ma.List(ma.Str(default="", missing=""))
    asset_id = ma.Str(default="", missing="")
    description = ma.Str(default="", missing="")
    monitoring = ma.Int(default=1, missing=1)



