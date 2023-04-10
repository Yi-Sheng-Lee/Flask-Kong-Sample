from common.dao.base_dao import BaseDao
from app.auth.model.models import User


class UserDao(BaseDao):
    def __init__(self):
        super().__init__(User)

    def set_filters(self, **kwargs):
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
                self.set_filter_field_eq(key, value)

    def get_active_user_by_username(self, username):
        return self.get_one_by_fields(name=username)

    def get_by_name(self, username):
        return self.get_all_by_fields(name=username)