from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.asset.service.company_service import get_company_kv_list, delete_company, get_company_by_filter, update_company, \
    add_company, get_company, active_company
from app.auth.util.decorator import error_handler, auth_required
from common.util.response_util import return_response
from app.operator_record.service.operator_record_service import add_record_to_db

import logging

logger = logging.getLogger(__name__)


class Company(Resource):
    @classmethod
    @auth_required("/company/company-manage", "VIEW")
    @error_handler
    def get(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the company")
            res = get_company(uid)
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, e)
            return return_response(False, e)

    @classmethod
    @auth_required("/company/company-manage", "CREATE")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to create the company")
            payload = request.get_json()
            res = add_company(**payload)
            add_record_to_db(True, action="CREATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(True, action="CREATE", error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/company/company-manage", "UPDATE")
    @error_handler
    def put(cls, uid):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to put the company")
            payload = request.get_json()
            res = update_company(uid, **payload)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])


class Companies(Resource):
    @classmethod
    @auth_required("/company/company-manage", "VIEW")
    @error_handler
    def post(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the company")
            payload = request.get_json()
            res = get_company_by_filter(**payload) if payload else get_company_by_filter()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])

    @classmethod
    @auth_required("/company/company-manage", "DELETE")
    @error_handler
    def delete(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to delete the company")
            payload = request.get_json()
            if not payload:
                add_record_to_db(True, action="DELETE")
                return return_response(True, [])
            res = delete_company(payload)
            add_record_to_db(True, action="DELETE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="DELETE", error=e.args[0])
            return return_response(False, e.args[0])


class CompanyMenu(Resource):
    @classmethod
    @jwt_required
    @error_handler
    def get(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to fetch the company menu list")
            res = get_company_kv_list()
            add_record_to_db(True)
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, error=e.args[0])
            return return_response(False, e.args[0])


class CompanyActive(Resource):
    @classmethod
    @auth_required("/company/company-manage", "UPDATE")
    @error_handler
    def put(cls):
        try:
            logger.info(f"[Resource] <{cls.__name__}> starts to active the company")
            payload = request.get_json()
            if not payload:
                add_record_to_db(True, action="UPDATE")
                return return_response(True, [])
            res = active_company(payload)
            add_record_to_db(True, action="UPDATE")
            return return_response(True, res)
        except Exception as e:
            logger.error(e, exc_info=True)
            add_record_to_db(False, action="UPDATE", error=e.args[0])
            return return_response(False, e.args[0])
