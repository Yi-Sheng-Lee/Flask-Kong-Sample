from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from common.util.response_util import return_response
from app.auth.util.decorator import auth_required, error_handler
from app.auth.service.role_service import (
    get_roles,
    get_roles_menu,
    get_role_permissions_by_uid,
    add_role_to_db,
    update_role_to_db,
    delete_role_from_db,
    get_permissions_menu,
)
from app.operator_record.service.operator_record_service import add_record_to_db
import logging

logger = logging.getLogger(__name__)


class PermissionsMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the menu")
            res = get_permissions_menu()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])


class RolesMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the menu")
            filters = {}
            if request.args.get("company_id"):
                filters["company_id"] = request.args.get("company_id")
            res = get_roles_menu(**filters) if filters else get_roles_menu()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])


class Roles(Resource):
    @classmethod
    @auth_required("/user/role-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch all data")
            req = request.get_json()
            res = get_roles(**req)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/role-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to delete bulk data")
            res = delete_role_from_db(**req)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class Role(Resource):
    @classmethod
    @auth_required("/user/role-manage", "VIEW")
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch one of data")
            res = get_role_permissions_by_uid(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/role-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to add data")
            res = add_role_to_db(**req)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/role-manage", "UPDATE")
    @error_handler
    def put(cls, uid):
        try:
            req = request.get_json()
            logger.info(f"[Resource] <{cls.__name__}> starts to update data")
            res = update_role_to_db(uid, **req)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/user/role-manage", "DELETE")
    @error_handler
    def delete(cls, uid):
        try:
            req = {"roles": [uid]}
            logger.info(f"[Resource] <{cls.__name__}> starts to delete data")
            res = delete_role_from_db(**req)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])
