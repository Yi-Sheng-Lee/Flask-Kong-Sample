from flask_jwt_extended import get_jwt_claims
from common.dao.base_dao import BaseDao
from app.auth.dao.user_dao import UserDao
from common.enum.code_enum import DeviceRegionLayer
from app.asset.model.models import Device
from sqlalchemy import or_, func
import logging

logger = logging.getLogger(__name__)


class DeviceDao(BaseDao):
    """
    Table device data access
    """

    def __init__(self):
        super().__init__(Device)
        self.user = UserDao().get_by_uid(self.claims.get("user_uid"))

    def get_all_by_fields(self, **kwargs):
        return super().get_all_by_fields(**kwargs)

    def set_filters(self, **kwargs):
        """
        設定過濾條件, 預設皆為 field == value

        權限設定:
        self.auth 表示需要限制model.company_id = login user company.id
        self.user_auth 表示需要限制 model.create_user = login user or device.manages = login user


        建立時間區間計算:
        kwargs內包含 start_time 會帶入 model.create_at >= start_time
        kwargs內包含 end_time 會帶入 model.create_at <= end_time

        :param kwargs:
        :return:
        """

        # 權限控管判斷
        if self.claims:
            # 是否為總管公司
            if not self.claims["is_admin_company"] and hasattr(self._model, "company_id"):
                logger.info(f"Set company auth company_id: {self.claims.get('company_id')}")
                self.filters.append(self._model.company_id == self.claims.get("company_id"))

            # 設備擁有者or管理員判斷
            # if self.user_auth and self.claims and not self.claims["is_admin"] and hasattr(self._model, "create_user"):
            if not self.claims["is_admin_company"] \
                    and not self.claims["is_admin"]\
                    and hasattr(self._model, "create_user"):
                logger.info(f"Set user auth user: {self.claims.get('user')}")
                self.filters.append(
                    or_(
                        self._model.create_user == self.claims.get("user"),
                        self._model.managers.contains(self.user)
                    )
                )

        for key, value in kwargs.items():
            if not value:
                continue

            # 判斷計算時間區間
            if key == 'start_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at >= value)
                continue

            if key == 'end_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at <= value)
                continue

            if key == "name":
                self.filters.append(self._model.name.like(f"%{value}%"))
                continue

            if key == "ip":
                # query_str = f"{value}"
                # if value.startswith('*'):
                #     query_str = "%" + query_str
                # if value.endswith('*'):
                #     query_str = query_str + "%"
                self.filters.append(self._model.ip.like(f"%{value}%"))
                continue

            self.set_filter_field_eq(key, value)

    def get_by_asset_id(self, asset_id):
        return self.get_one_by_fields(asset_id=asset_id)
    
    def get_by_ip(self, ip):
        return self.get_one_by_fields(ip=ip)

    def get_monitoring_devices(self, monitoring=1):
        return self.get_all_by_fields(monitoring=monitoring)

    def get_sensor_monitoring_devices(self, sensor_uid, monitoring=1):
        return self.get_all_by_fields(monitoring=monitoring, sensor_uid=sensor_uid)

    def get_devices_count_by_region_layer(self, layer=DeviceRegionLayer.GROUP.value, **kwargs):
        layer_fields = (
            Device.country_code,
            Device.city_code,
            Device.zip_code,
            Device.company_id,
            Device.sensor_id,
            Device.group_id,
        )

        self.filters.append(Device.sensor.city_code.isnot(None))

        self.set_filters(**kwargs)

        res = Device.query.with_entities(
            *layer_fields[:layer],
            func.count(Device.id).label("count")
        ).filter(
            *self.filters
        ).group_by(
            *layer_fields[:layer]
        ).order_by(
            *layer_fields[:layer]
        ).all()

        return res

    def get_sensor_device(self, sensor_uid="", country_code='', city_code=''):
        """
        取得Sensor device data, 其中country_code, city_code 為選填
        :param sensor_uid:
        :param country_code:
        :param city_code:
        :return:
        """
        self.set_filters(
            sensor_uid=sensor_uid
        )

        if country_code:
            self.filters.append(Device.sensor.country_code == country_code)

        if city_code:
            self.filters.append(Device.sensor.city_code == city_code)

        self.order_by_fields.append("group_id")
        self.order_by_fields.append("ip")

        res = self.get_all_by_fields({})

        return res

    def get_device_by_ip_sensor_id(self, ip, sensor_id):
        res = self.get_one_by_fields(ip=ip, sensor_id=sensor_id)
        return res

    def update_devices_group(self, device_uids, group_id):
        Device.query.filter(Device.uid.in_(device_uids)).update({
            Device.group_id: group_id,
            Device.update_user: self.user.name
        }, synchronize_session=False)
        return super().commit()