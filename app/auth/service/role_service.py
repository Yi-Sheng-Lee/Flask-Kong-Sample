import json
import traceback

from flask_jwt_extended import get_jwt_claims

from app.auth.dao.operation_dao import OperationDao
from app.auth.dao.permission_dao import PermissionDao
from app.auth.dao.role_dao import RoleDao
from app.auth.dao.role_permission_dao import RolePermissionDao
from common.enum.service_enum import ServiceError
from app.auth.model.models import Role, RolePermission
from app.auth.schema.schemas import (
    RoleSchema,
    RoleBulkSchema,
    RoleFieldSchema,
    RolePermissionSchema, PermissionSchema, OperationSchema,
)
import logging
import copy

from config.auth_unwanted import AUTH_UNWANTED

logger = logging.getLogger(__name__)


def permissions_operations_list_builder():
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    auth_unwanted = AUTH_UNWANTED
    data = {}

    all_permissions = PermissionDao().get_permissions_all()

    if company_id > 1:
        p_list = [json.loads(PermissionSchema().dumps(p)) for p in all_permissions if p.id != 9 and p.enable != 0]
    else:
        p_list = [json.loads(PermissionSchema().dumps(p)) for p in all_permissions if p.enable != 0]

    data["permissions"] = p_list

    for p_data in data["permissions"]:
        if "operations" not in p_data.keys():
            o_list = []
            for o in OperationDao().get_operations_all():
                o_dict = json.loads(OperationSchema().dumps(o))
                o_dict["status"] = 0
                o_list.append(o_dict)
            o_list = [operation for operation in o_list if operation["id"] not in auth_unwanted[p_data["id"]]]
            p_data["operations"] = o_list

    return data


def get_roles(**kwargs):
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    role_dao = RoleDao()
    data = []
    for k, v in kwargs.items():
        role_dao.set_filter_field_like(k, v)

    role_dao.set_order_by(["company_id"])
    roles = role_dao.get_all_by_fields() if company_id == 1 else role_dao.get_all_by_fields(company_id=company_id)
    role_list_schema = RoleSchema(exclude=["id"])
    for role in roles:
        temp = role_list_schema.dump(role)
        temp["user_count"] = len(role.users)
        data.append(temp)
    return data


def get_roles_menu(**kwargs):
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    role_dao = RoleDao()
    role_dao.set_order_by(['company_id'])
    roles = role_dao.get_all_by_fields(**kwargs) if company_id == 1 else RoleDao().get_all_by_fields(company_id=company_id)
    role_menu_schema = RoleSchema(only=["name", "uid", "company_name"])
    return role_menu_schema.dump(roles, many=True)


def get_permissions_menu():
    return permissions_operations_list_builder()


def get_role_permissions_by_id(id):
    role_dao = RoleDao()
    role_permission_list = role_dao.get_permissions_operations_by_id(id)
    keys = ("id", "uid", "name", "description", "id", "name", "url", "id", "name")
    data = {}
    if role_permission_list:
        data = permissions_operations_list_builder()
        for role in role_permission_list:
            temp_all = list(zip(keys, role))
            temp_p = dict(temp_all[4:7])
            temp_o = dict(temp_all[-2:])
            if "id" not in data:
                data.update(temp_all[0:4])
            for p_i, p_data in enumerate(data["permissions"]):
                if p_data["id"] == temp_p["id"]:
                    for o_data in data["permissions"][p_i]["operations"]:
                        if o_data["id"] == temp_o["id"]:
                            o_data["status"] = 1
        del data["id"]
    return data


def get_role_permissions_by_uid(uid):
    role_dao = RoleDao()
    role_permission_list = role_dao.get_permissions_operations_by_uid(uid)
    role_info = RoleSchema().dump(role_dao.get_one_by_fields(uid=uid))
    keys = ("id", "uid", "name", "description", "id", "name", "url", "id", "name")
    data = {}
    if role_permission_list:
        data = permissions_operations_list_builder()
        for role in role_permission_list:
            temp_all = list(zip(keys, role))
            temp_p = dict(temp_all[4:7])
            temp_o = dict(temp_all[-2:])
            if "id" not in data:
                data.update(temp_all[0:4])
            for p_i, p_data in enumerate(data["permissions"]):
                if p_data["id"] == temp_p["id"]:
                    for o_data in data["permissions"][p_i]["operations"]:
                        if o_data["id"] == temp_o["id"]:
                            o_data["status"] = 1
        del data["id"]
        data["company_name"] = role_info["company_name"]
    return data


def add_role_permission_to_db(role_dao, role_id, auth_args):
    role_permissions = []
    role_permission_schema = RolePermissionSchema()
    for auth_arg in auth_args:
        auth_arg["roles_id"] = role_id
        role_permission = role_permission_schema.load(auth_arg)
        role_permissions.append(role_permission)
    role_dao.add_all(role_permissions)


def add_role_to_db(**kwargs):
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    role_field_schema = RoleFieldSchema()
    role_args = role_field_schema.load(kwargs)
    auth_args = copy.deepcopy(role_args)
    role_dao = RoleDao()
    role_schema = RoleSchema()
    role_args.pop("auth")
    role = role_schema.load(role_args)
    role.company_id = company_id
    try:
        role_dao.add(role)
    except Exception:
        raise
    else:
        role_id = role_dao.get_one_by_fields(name=role.name).id
        add_role_permission_to_db(role_dao, role_id, auth_args["auth"])
    return get_role_permissions_by_id(role_id)


def update_role_to_db(uid, **kwargs):
    # claims = get_jwt_claims()
    # company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    role_field_schema = RoleFieldSchema()
    role_args = role_field_schema.load(kwargs)
    role_dao = RoleDao()
    role = role_dao.get_one_by_fields(uid=uid)
    role.name = role_args["name"]
    role.description = role_args["description"]
    # role.company_id = company_id
    role_dao.update(role)
    try:
        RolePermissionDao().delete_role_permissions_by_roles_id(role.id)
    except Exception:
        raise
    else:
        add_role_permission_to_db(role_dao, role.id, role_args["auth"])
    return get_role_permissions_by_id(role.id)


def delete_role_from_db(**args):
    role_bulk_schema = RoleBulkSchema()
    roles = role_bulk_schema.load(args).get("roles")
    for role_uid in roles:
        role_dao = RoleDao()
        role = role_dao.get_one_by_fields(uid=role_uid)
        if len(role.users):
            raise Exception(ServiceError.ROLE_IN_USED.value)
        role_permissions = RolePermissionDao().get_role_permissions_by_roles_id(role.id)
        try:
            for role_permission in role_permissions:
                role_dao.delete(role_permission)
        except Exception:
            raise
        else:
            role_dao.delete(role)
    return args


def init_company_admin_role(company_id):
    admin_role = Role()
    admin_role.company_id = company_id
    admin_role.name = "Administrator"
    admin_role.description = "Administrator"
    RoleDao().add(admin_role)

    tmp_admin_role_permissions = RolePermissionDao().get_role_permissions_by_roles_id(1)

    if admin_role.id:
        for permission in tmp_admin_role_permissions:
            if permission.permissions_id == 9:
                continue
            rp = RolePermission()
            rp.roles_id = admin_role.id
            rp.is_revoked = 0
            rp.permissions_id = permission.permissions_id
            rp.operations_id = permission.operations_id
            RoleDao().add(rp)

    return admin_role
