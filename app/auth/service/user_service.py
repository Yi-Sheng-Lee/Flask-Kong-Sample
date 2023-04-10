from marshmallow import INCLUDE
from sqlalchemy import desc

from app.auth.dao.role_dao import RoleDao
from app.auth.dao.user_dao import UserDao
from flask_jwt_extended import get_jwt_identity, get_jwt_claims

# from app.dashboard.service.user_dashboard_service import init_user_dashboard
from common.enum.service_enum import ServiceError
from app.auth.model.models import User
from app.auth.schema.schemas import UserSchema, UserBulkSchema, UserFieldSchema
from app.auth.service.role_service import get_role_permissions_by_id
import logging
import bcrypt
import uuid

logger = logging.getLogger(__name__)


def get_users(**kwargs):
    user_list_schema = UserSchema()
    claims = get_jwt_claims()
    user_dao = UserDao()

    # 修改成本公司
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    # 載入 filter kv
    for key, value in kwargs.items():
        user_dao.set_filter_field_like(key, value)

    user_dao.set_order_by(["company_id"])
    users = user_dao.get_all_by_fields() if company_id == 1 else user_dao.get_all_by_fields(company_id=company_id)
    data = []

    for user in users:
        temp = user_list_schema.dump(user)
        login_records = user.login_records.order_by(desc("last_login")).first()
        temp["last_login"] = login_records.last_login.strftime("%Y-%m-%d %H:%M:%S") if login_records else ""
        data.append(temp)
    return data


def get_users_menu(**kwargs):
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0

    user_menu_schema = UserSchema(only=["uid", "name", "company_name"])
    user_dao = UserDao()
    user_dao.set_order_by(["company_id"])
    users = user_dao.get_all_by_fields(**kwargs, is_delete=0) if company_id == 1 else UserDao().get_all_by_fields(company_id=company_id, is_delete=0)
    return user_menu_schema.dump(users, many=True)


def get_user_by_uid(user_uid):
    user_dao = UserDao()
    user = user_dao.get_by_uid(user_uid)
    role_name = user.role.name
    user_schema = UserSchema()
    data = user_schema.dump(user)
    data["role_name"] = role_name
    current_user = get_jwt_identity()
    if current_user == user_uid:
        data["permissions"] = get_role_permissions_by_id(data["role_id"])["permissions"]
    return data


def add_user_to_db(**kwargs):
    user_field_schema = UserFieldSchema()
    user_args = user_field_schema.load(kwargs)
    user_dao = UserDao()
    exist_user = user_dao.get_active_user_by_username(user_args.get('name'))
    if exist_user:
        raise Exception(ServiceError.USERNAME_EXIST.value)

    if not kwargs.get('company_id'):
        claims = get_jwt_claims()
        company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    else:
        company_id = kwargs.get('company_id')

    role = RoleDao().get_one_by_fields(uid=user_args.get('role_uid'), company_id=company_id)
    if not role:
        raise Exception(ServiceError.ROLE_NOT_EXIST.value)

    user_args["uid"] = str(uuid.uuid4())

    user = User()
    user.name = user_args.get('name')
    user.password = bcrypt.hashpw(kwargs["password"].encode("utf-8"), bcrypt.gensalt())
    user.company_id = company_id
    user.roles_id = role.id
    user.nickname = user_args.get('nickname')
    user.email = user_args.get('email')
    user.phone = user_args.get('phone')
    user.is_admin = user_args.get('is_admin')

    try:
        user_dao.add(user)

        # init default dashboard
        # init_user_dashboard(user.uid)
    except Exception as e:
        logger.error(e)
        raise
    return get_user_by_uid(user.uid)


def update_user_to_db(user_uid, **kwargs):
    user_field_schema = UserFieldSchema(exclude=["password", "old_password"])
    user_args = user_field_schema.load(kwargs)
    user_dao = UserDao()
    user = user_dao.get_by_uid(user_uid)
    if user_args.get("new_password"):
        hashed = bcrypt.hashpw(
            user_args["new_password"].encode("utf-8"), bcrypt.gensalt()
        )
        user.password = hashed.decode("utf-8")

    role = RoleDao().get_one_by_fields(uid=user_args.get('role_uid'))
    if not role:
        raise Exception(ServiceError.ROLE_NOT_EXIST.vaule)

    user.name = user_args["name"]
    user.nickname = user_args["nickname"]
    user.phone = user_args["phone"]
    user.email = user_args["email"]
    user.roles_id = role.id
    user_dao.update(user_dao)
    return get_user_by_uid(user_uid)


def update_user_profile_to_db(**kwargs):
    user_field_schema = UserFieldSchema(exclude=["password"])
    claims = get_jwt_claims()
    user_uid = claims["user_uid"]
    user_args = user_field_schema.load(kwargs)
    user_dao = UserDao()
    user = user_dao.get_by_uid(user_uid)

    if user_args.get("old_password") and user_args.get("new_password"):
        if not bcrypt.checkpw(
                user_args["old_password"].encode("utf-8"), user.password.encode("utf-8")
        ):
            raise ValueError("old_password")
        hashed = bcrypt.hashpw(
            user_args["new_password"].encode("utf-8"), bcrypt.gensalt()
        )
        user.password = hashed.decode("utf-8")

    role = RoleDao().get_one_by_fields(uid=user_args.get('role_uid'))
    if not role:
        raise Exception(ServiceError.ROLE_NOT_EXIST.vaule)

    user.name = user_args["name"]
    user.nickname = user_args["nickname"]
    user.phone = user_args["phone"]
    user.email = user_args["email"]
    user.roles_id = role.id
    user_dao.update(user_dao)
    return get_user_by_uid(user_uid)


def set_user_is_delete(**kwargs):
    user_bulk_schema = UserBulkSchema()
    users = user_bulk_schema.load(kwargs).get("users")

    for user_uid in users:
        user_dao = UserDao()
        user = user_dao.get_by_uid(user_uid)
        user.is_delete = 1
        user_dao.update(user)
    return True


def delete_user_from_db(**args):
    user_bulk_schema = UserBulkSchema()
    users = user_bulk_schema.load(args).get("users")
    for user_uid in users:
        user_dao = UserDao()
        user = user_dao.get_by_uid(user_uid)
        user_dao.delete(user)
    return args
