from common.dao.base_dao import BaseDao
from app.auth.model.models import RolePermission
from app import db


class RolePermissionDao(BaseDao):
    """
    Table role permission data access
    """

    def __init__(self):
        super().__init__(RolePermission)

    def get_role_permissions_by_roles_id(self, roles_id):
        return self.get_all_by_fields(roles_id=roles_id, is_revoked=0)

    def get_role_permissions_by_roles_id_with_unrevoked(self, roles_id):
        return self.get_all_by_fields(roles_id=roles_id, is_revoked=0)

    def delete_role_permissions_by_roles_id(self, roles_id):
        """
        刪除 role permission by role_id
        :param roles_id:
        :return:
        """
        self._model.query.filter_by(roles_id=roles_id).delete()
        super().commit()
        return True