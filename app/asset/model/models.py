from sqlalchemy.ext.associationproxy import association_proxy
from app import db
from common.util.common_util import generate_uuid
from datetime import datetime

device_managers = db.Table(
    "device_managers",
    db.Column("device_id", db.Integer, db.ForeignKey("devices.id"), nullable=False, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True)
)


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False, default=generate_uuid)
    pid = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_tel = db.Column(db.String(255))
    tax_id = db.Column(db.String(255))
    country_code = db.Column(db.String(6), nullable=False, server_default='TW')
    city_code = db.Column(db.String(6), nullable=False, server_default='TPE')
    zip_code = db.Column(db.String(6), nullable=False, server_default='100')
    address = db.Column(db.String(255))
    description = db.Column(db.String(255))
    is_revoke = db.Column(db.Integer, default=0, server_default="0")
    is_admin = db.Column(db.Integer, default=0, server_default="0")
    create_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
    sensors = db.relationship(
        "Sensor",
        backref='companies',
        primaryjoin='Company.id==Sensor.company_id',
        foreign_keys='Sensor.company_id',
        lazy=True,
        uselist=True
    )


class Sensor(db.Model):
    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False, default=generate_uuid)
    pid = db.Column(db.Integer, nullable=False, default=0)
    ip = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(255), default='avt', server_default='avt')
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, default=0, server_default='0')
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    country_code = db.Column(db.String(6), nullable=False, default="TW", server_default="TW")
    city_code = db.Column(db.String(6), nullable=False, default="TPE", server_default="TPE")
    zip_code = db.Column(db.String(6), nullable=False, default="103", server_default="103")
    address = db.Column(db.String(500))
    create_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
    company = db.relationship("Company", lazy=True)
    devices = db.relationship(
        "Device",
        backref='sensors',
        primaryjoin='Sensor.id==Device.sensor_id',
        foreign_keys='Device.sensor_id',
        lazy=True,
        uselist=True
    )
    company_uid = association_proxy('company', 'uid')
    company_name = association_proxy('company', 'name')


class DeviceGroup(db.Model):
    __tablename__ = "device_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    uid = db.Column(db.String(255), nullable=False, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False, default='IT')
    sort = db.Column(db.Integer, nullable=False, default=1)
    is_default = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    has_topology = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    topology_img = db.Column(db.Text(16777216))
    description = db.Column(db.String(500))
    devices = db.relationship(
        "Device",
        backref='device_groups',
        primaryjoin='DeviceGroup.id==Device.group_id',
        foreign_keys='Device.group_id',
        lazy=True,
        uselist=True
    )
    device_topology = db.relationship("DeviceGroupTopology", lazy=True)
    create_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
    company = db.relationship("Company", lazy=True)
    company_uid = association_proxy('company', 'uid')



class DeviceGroupTopology(db.Model):
    __tablename__ = "device_group_topology"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False, default=generate_uuid)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    group_id = db.Column(db.Integer, db.ForeignKey("device_groups.id"), nullable=False, server_default='0')
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False, server_default='0')
    lat = db.Column(db.String(20), default='0.0', server_default='0.0')
    lng = db.Column(db.String(20), default='0.0', server_default='0.0')
    create_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False, default=generate_uuid)
    asset_id = db.Column(db.String(255))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    sensor_id = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    group_id = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    name = db.Column(db.String(255), nullable=False)
    hostname = db.Column(db.String(255), default="")
    os = db.Column(db.String(255), default="")
    ip = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), default="")
    monitoring = db.Column(db.Integer, nullable=False, default=1, server_default="1")
    description = db.Column(db.String(500))
    create_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_user = db.Column(db.String(255), default='system', nullable=False, server_default='system')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
    company = db.relationship("Company", lazy=True)
    sensor = db.relationship(
        "Sensor",
        primaryjoin='Device.sensor_id==Sensor.id',
        foreign_keys='Device.sensor_id',
        uselist=False,
        lazy=True
    )
    group = db.relationship(
        "DeviceGroup",
        primaryjoin='Device.group_id==DeviceGroup.id',
        foreign_keys='Device.group_id',
        uselist=False,
        lazy=True
    )
    topology = db.relationship("DeviceGroupTopology", lazy=True, uselist=False, cascade="all, delete-orphan")
    managers = db.relationship(
        "User",
        secondary=device_managers,
        backref=db.backref("devices", lazy=True),
    )
    company_uid = association_proxy('company', 'uid')
    group_uid = association_proxy('group', 'uid')
    sensor_uid = association_proxy('sensor', 'uid')
    lat = association_proxy('topology', 'lat')
    lng = association_proxy('topology', 'lng')
