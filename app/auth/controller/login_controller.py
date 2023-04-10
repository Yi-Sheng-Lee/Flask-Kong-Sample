from app import jwt
from flask import request
from flask_restful import Resource
from app.auth.util.decorator import error_handler
from common.util.response_util import return_response
from common.enum.controller_error_enum import ControllerErrorEnum
from app.auth.service.login_token_service import (
    authenticate,
    refresh_user_token,
    revoke_token,
    is_token_revoked,
    get_user_auth_by_identity,
)
from app.auth.service.user_service import (
    get_user_by_uid
)
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_raw_jwt
from app.operator_record.service.operator_record_service import add_record_to_db
import logging

logger = logging.getLogger(__name__)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user_auth = get_user_auth_by_identity(identity)
    user = get_user_by_uid(identity)
    user_data = {
        "auth": user_auth,
        "user": user["name"],
        "user_uid": user["uid"],
        "company_id": user["company_id"],
        "is_admin_company": True if user['is_admin_company'] else False,
        "is_admin": True if user["is_admin"] else False
    }
    return user_data


@jwt.unauthorized_loader
def missing_token_callback(error):
    add_record_to_db(False, action="LOGIN", error=ControllerErrorEnum.UNAUTHORIZED.value)
    return return_response(False, ControllerErrorEnum.UNAUTHORIZED.value)


@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
    return return_response(False, ControllerErrorEnum.INVALID_TOKEN.value)


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token["type"]
    if token_type == "refresh":
        add_record_to_db(False, action="REFRESH", error=ControllerErrorEnum.REFRESH_TOKEN_EXPIRED.value)
        return return_response(False, ControllerErrorEnum.REFRESH_TOKEN_EXPIRED.value)
    else:
        add_record_to_db(False, action="REFRESH", error=ControllerErrorEnum.ACCESS_TOKEN_EXPIRED.value)
        return return_response(False, ControllerErrorEnum.ACCESS_TOKEN_EXPIRED.value)


@jwt.revoked_token_loader
def revoked_token_callback():
    add_record_to_db(False, action="REFRESH", error=ControllerErrorEnum.ACCESS_TOKEN_REVOKED.value)
    return return_response(False, ControllerErrorEnum.ACCESS_TOKEN_REVOKED.value)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    add_record_to_db(False, action="REFRESH", error=ControllerErrorEnum.NEED_FRESH_TOKEN.value)
    return return_response(False, ControllerErrorEnum.NEED_FRESH_TOKEN.value)


class Login(Resource):
    @classmethod
    @error_handler
    def post(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to login")
            res = authenticate(**req)
            add_record_to_db(True, action="LOGIN")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="LOGIN", error=e.args[0])
            return return_response(False, e.args[0])


class LoginRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to refresh user token")
            add_record_to_db(True, action="REFRESH")
            return return_response(True, refresh_user_token())
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="REFRESH", error=e.args[0])
            return return_response(False, e.args[0])


class Logout(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def post(cls):
        logger.info(f"[Resource] <{cls.__name__}> starts to logout")
        res = revoke_token(get_raw_jwt(), 1)
        add_record_to_db(True, action="LOGOUT")
        return return_response(True, res)
