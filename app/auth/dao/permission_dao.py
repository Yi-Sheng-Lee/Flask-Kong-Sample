from common.dao.base_dao import BaseDao
from app.auth.model.models import Permission
from app import db


class PermissionDao(BaseDao):
    """
    Table permission data access
    """

    def __init__(self):
        super().__init__(Permission)

    def get_by_name(self, name):
        return self.get_all_by_fields(name=name).first()

    def get_permissions_all(self):
        return self.get_all_by_fields()

