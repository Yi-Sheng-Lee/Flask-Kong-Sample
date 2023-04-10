from common.dao.base_dao import BaseDao
from app.operator_record.model.models import UserOperationRecord
import logging

logger = logging.getLogger(__name__)


class UserOperationRecordDao(BaseDao):
    def __init__(self):
        super().__init__(UserOperationRecord)

    def set_filters(self, **kwargs):
        """
        設定過濾條件, 預設皆為 field == value

        權限設定:
        self.auth 表示需要限制model.company_id = login user company.id
        self.user_auth 表示需要限制model.create_user = login user

        建立時間區間計算:
        kwargs內包含 start_time 會帶入 model.create_at >= start_time
        kwargs內包含 end_time 會帶入 model.create_at <= end_time

        :param kwargs:
        :return:
        """

        if self.claims:
            # 判斷是否為總公司
            if not self.claims["is_admin_company"] and hasattr(self._model, "company_id"):
                logger.info(f"Set company auth company_id: {self.claims.get('company_id')}")
                self.filters.append(self._model.company_id == self.claims.get("company_id"))

            # 判斷是否要受到資料擁有者限制
            if self.user_auth and not self.claims["is_admin"] and hasattr(self._model, "create_user"):
                logger.info(f"Set user auth user: {self.claims.get('user')}")
                self.filters.append(self._model.create_user == self.claims.get("user"))

        for key, value in kwargs.items():
            if value == '':
                continue

            # 判斷計算時間區間
            if key == 'start_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at >= value)
                continue

            if key == 'end_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at <= value)
                continue

            if hasattr(self._model, key):
                if key == 'web_url' and value is not '/':
                    self.set_filter_field_like(key, value)
                else:
                    self.set_filter_field_eq(key, value)

    def get_all_by_fields(self, **kwargs):
        return super().get_all_by_fields(**kwargs)
