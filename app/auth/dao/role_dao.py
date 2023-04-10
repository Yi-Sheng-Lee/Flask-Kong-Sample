from common.dao.base_dao import BaseDao
from app.auth.model.models import Role, RolePermission, Permission, Operation, User
from app import db


class RoleDao(BaseDao):
    """
    Table command_action_log data access
    """

    def __init__(self):
        super().__init__(Role)

    @classmethod
    def get_role_permissions_by_roles_id(cls, roles_id):
        return RolePermission.query.filter_by(roles_id=roles_id, is_revoked=0).all()

    @classmethod
    def get_role_permissions_by_roles_id_with_unrevoked(cls, roles_id):
        return RolePermission.query.filter_by(roles_id=roles_id, is_revoked=0).all()

    @classmethod
    def get_permissions_operations_by_id(cls, role_id):
        res = (
            db.session.query(
                Role.id,
                Role.uid,
                Role.name,
                Role.description,
                Permission.id,
                Permission.name,
                Permission.url,
                Operation.id,
                Operation.name,
            )
            .join(RolePermission, Role.id == RolePermission.roles_id)
            .join(Permission, Permission.id == RolePermission.permissions_id)
            .join(Operation, Operation.id == RolePermission.operations_id)
            .filter(Role.id == role_id, RolePermission.is_revoked == 0)
            .order_by(Permission.id, Operation.id)
            .all()
        )
        return res

    @classmethod
    def get_permissions_operations_by_uid(cls, uid):
        res = (
            db.session.query(
                Role.id,
                Role.uid,
                Role.name,
                Role.description,
                Permission.id,
                Permission.name,
                Permission.url,
                Operation.id,
                Operation.name,
            )
                .join(RolePermission, Role.id == RolePermission.roles_id)
                .join(Permission, Permission.id == RolePermission.permissions_id)
                .join(Operation, Operation.id == RolePermission.operations_id)
                .filter(Role.uid == uid, RolePermission.is_revoked == 0)
                .order_by(Permission.id, Operation.id)
                .all()
        )
        return res

    @classmethod
    def get_permission_operation_users(cls, permission_id, operation_id):
        res = (
            db.session.query(
                User.name,
                User.email,
                User.uid,
                Role.id,
                Role.name,
                Role.description,
                Permission.id,
                Permission.name,
                Permission.url,
                Operation.id,
                Operation.name
            )
                .join(RolePermission, Role.id == RolePermission.roles_id)
                .join(Permission, Permission.id == RolePermission.permissions_id)
                .join(Operation, Operation.id == RolePermission.operations_id)
                .join(User, User.roles_id == Role.id)
                .filter(RolePermission.is_revoked == 0,
                        RolePermission.permissions_id == permission_id,
                        RolePermission.operations_id == operation_id,
                        User.is_delete == 0,
                        )
                .order_by(Permission.id, Operation.id)
                .all()
        )
        return res
