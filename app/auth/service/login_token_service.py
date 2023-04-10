from datetime import datetime, timezone
# import datetime
import jwt
import uuid

import traceback

import bcrypt

import requests
from flask import current_app

from app.auth.dao.user_dao import UserDao
from app.auth.dao.role_dao import RoleDao
from app.auth.dao.login_token_dao import LoginTokenDao
from common.enum.controller_error_enum import ControllerErrorEnum
from app.auth.schema.schemas import LoginFieldSchema, LoginTokenSchema, LoginRecordSchema
from flask_jwt_extended import (
    get_jwt_identity,
    decode_token,
)
from common.enum.api_enum import KongApi


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc)


def prune_db():
    login_token_dao = LoginTokenDao()
    expired = login_token_dao.get_by_expired_time()
    for token in expired:
        login_token_dao.delete(token)


def get_login_tokens():
    login_token_dao = LoginTokenDao()
    login_tokens = login_token_dao.get_all_by_fields()
    login_token_schema = LoginTokenSchema()
    return [login_token_schema.dump(login_token) for login_token in login_tokens]


def get_user_tokens_by_identity(user_identity):
    login_token_dao = LoginTokenDao()
    login_tokens = login_token_dao.get_by_user_identity(user_identity)
    login_token_schema = LoginTokenSchema()
    return [login_token_schema.dump(login_token) for login_token in login_tokens]


def get_user_auth_by_identity(user_identity):
    user_dao = UserDao()
    user = user_dao.get_by_uid(user_identity)
    role_dao = RoleDao()
    role_permission_list = role_dao.get_permissions_operations_by_id(user.roles_id)
    auths = {}
    for auth in role_permission_list:
        if auth["url"] not in auths:
            auths[auth["url"]] = [auth["name"]]
        else:
            auths[auth["url"]].append(auth["name"])
    return auths


def add_token_to_db(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)
    expires = _epoch_utc_to_datetime(decoded_token["exp"])
    data = {
        "jti": decoded_token["jti"],
        "token_type": decoded_token["type"],
        "user_identity": decoded_token[identity_claim],
        "expires": str(expires),
        "is_revoked": 0,
    }
    login_token_schema = LoginTokenSchema()
    login_token = login_token_schema.load(data)
    login_token_dao = LoginTokenDao()
    login_token_dao.add(login_token)
    return data


def is_token_revoked(decoded_token):
    jti = decoded_token["jti"]
    login_token_dao = LoginTokenDao()
    data = login_token_dao.get_by_jti(jti)
    # return data["is_revoked"]
    return data.is_revoked


def revoke_token(decoded_token, status):
    jti = decoded_token["jti"]
    identity = decoded_token["identity"]
    login_token_dao = LoginTokenDao()
    login_tokens = login_token_dao.get_by_user_identity_and_unrevoked(identity)
    res = []
    for login_token in login_tokens:
        login_token.is_revoked = status
        login_token_dao.update(login_token)
        login_token = login_token_dao.get_by_user_identity_and_jti(identity, jti)
        login_token_schema = LoginTokenSchema(only=["is_revoked", "expires"])
        res.append(login_token_schema.dump(login_token))
    return res


def refresh_user_token():
    current_user = get_jwt_identity()
    user_dao = UserDao()
    user = user_dao.get_by_uid(current_user)
    # new_access_token = create_access_token(identity=current_user, fresh=False)
    new_access_token = create_access_jwt_token(user, "access", False)
    add_token_to_db(new_access_token, "identity")
    return {"access_token": new_access_token}


def authenticate(**kwargs):
    login_field_schema = LoginFieldSchema()
    login_field_args = login_field_schema.load(kwargs)
    user_dao = UserDao()
    try:
        user = user_dao.get_active_user_by_username(login_field_args["username"])
        if not user:
            raise Exception(ControllerErrorEnum.AUTHENTICATION_FAILED.value)

        if user.company.is_revoke:
            raise Exception(ControllerErrorEnum.COMPANY_HAS_BEEN_REVOKED.value)

        if not bcrypt.checkpw(login_field_args["password"].encode("utf-8"), user.password.encode("utf-8")):
            raise Exception(ControllerErrorEnum.AUTHENTICATION_FAILED.value)

        access_token = create_access_jwt_token(user, "access", True)
        refresh_token = create_access_jwt_token(user, "refresh", False)
        add_token_to_db(access_token, "identity")
        add_token_to_db(refresh_token, "identity")
    except Exception as e:
        traceback.print_exc()
        raise e
    else:
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "uid": user.uid,
        }

        # if "dashboard" in current_app.blueprints.keys():
        #     from app.dashboard.dao.user_dashboard_dao import UserDashboardDao
        #     dashboards = UserDashboardDao().get_all_by_fields(user_id=user.id)
        #     if dashboards:
        #         data["default_dashboard_uid"] = dashboards[0].uid

        login_record_args = {"token": access_token, "user_id": user.id}
        login_record_schema = LoginRecordSchema()
        login_record = login_record_schema.load(login_record_args)
        login_token_dao = LoginTokenDao()
        login_token_dao.add(login_record)
    return data


def create_access_jwt_token(user_info, types, fresh):
    # 從 kong 取得該 user 相對應的 consumer 資訊，以 username 當作 key 查詢
    kong_url = KongApi.CONSUMER_JWT.value
    kong_jwt_path = kong_url.format(url=current_app.config["KONG_URL"], consumer=user_info.name)
    r = requests.get(kong_jwt_path)

    # 取得當前 UTC 時間
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = int(utc_time.timestamp())

    # user claims payload
    user_data = {
        "auth": get_user_auth_by_identity(user_info.uid),
        "user": user_info.name,
        "user_uid": user_info.uid,
        "company_id": user_info.company_id,
        "is_admin_company": True if user_info.is_admin_company else False,
        "is_admin": True if user_info.is_admin else False
    }

    # 產生 jwt payload
    payload = {
        "iss": r.json()["data"][0]["key"],
        "iat": utc_timestamp,
        "nbf": utc_timestamp,
        "jti": str(uuid.uuid4()),
        "exp": utc_timestamp + (current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] if types == "access" else current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]),
        "identity": user_info.uid,
        "type": types
    }
    if types == "access":
        payload["user_claims"] = user_data
        payload["fresh"] = fresh

    # 產生 JWT token
    jwt_token = jwt.encode(payload, r.json()["data"][0]["secret"], algorithm="HS256")

    return jwt_token.decode("utf-8")
