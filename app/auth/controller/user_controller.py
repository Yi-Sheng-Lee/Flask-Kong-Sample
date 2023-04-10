from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from common.util.response_util import return_response
from app.auth.util.decorator import auth_required, error_handler
from app.auth.service.user_service import (
    get_users,
    get_users_menu,
    get_user_by_uid,
    add_user_to_db,
    update_user_to_db,
    delete_user_from_db,
    update_user_profile_to_db
)

from app.operator_record.service.operator_record_service import add_record_to_db
import logging

logger = logging.getLogger(__name__)


class UsersMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the menu")
            filters = {}
            if request.args.get("company_id"):
                filters["company_id"] = request.args.get("company_id")
            res = get_users_menu(**filters) if filters else get_users_menu()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])


class Users(Resource):
    @classmethod
    @auth_required("/user/user-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch all data")
            req = request.get_json()
            res = get_users(**(req or {}))
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/user-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to delete bulk data")
            res = delete_user_from_db(**req)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class User(Resource):
    @classmethod
    @auth_required("/user/user-manage", "VIEW")
    @error_handler
    def get(cls, user_uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch one of data")
            res = get_user_by_uid(user_uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/user-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to add data")
            res = add_user_to_db(**req)
            add_record_to_db(False, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, str(e))

    @classmethod
    @auth_required("/user/user-manage", "UPDATE")
    @error_handler
    def put(cls, user_uid):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to update data")
            res = update_user_to_db(user_uid, **req)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/user-manage", "DELETE")
    @error_handler
    def delete(cls, user_uid):
        try:
            req = {"users": [user_uid]}
            logger.info(f"[Resource] <{cls.__name__}> starts to delete data")
            res = delete_user_from_db(**req)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class UserProfile(Resource):
    @classmethod
    @auth_required()
    @error_handler
    def put(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to update data")
            res = update_user_profile_to_db(**req)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])
