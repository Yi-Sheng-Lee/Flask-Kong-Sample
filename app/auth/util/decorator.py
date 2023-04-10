from flask import session, request
from functools import wraps
from marshmallow import ValidationError
from ipaddress import AddressValueError
from app.auth.dao.user_dao import UserDao
from common.enum.dao_error_enum import BaseDaoError
from common.util.response_util import return_response
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import UnmappedInstanceError
from common.util.common_util import email_regex, ip_regex
from common.enum.controller_error_enum import ControllerErrorEnum
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, get_jwt_identity
import functools
import logging
import re

logger = logging.getLogger(__name__)


def re_for_error_message(msg_string):
    return re.findall(r"\'(\S+)\'", msg_string)[0]


def auth_required(permission=None, operation=None):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            current_user = get_jwt_identity()
            req_user = UserDao().get_active_user_by_username(claims["user"])
            if (req_user.is_admin or (permission is None and operation is None)):
                return fn(*args, **kwargs)
            auths = claims['auth']
            if (permission in auths.keys() and operation in auths[permission]) or (
                kwargs.get("user_uid") and kwargs.get("user_uid") == current_user
            ):
                return fn(*args, **kwargs)
            return return_response(False, ControllerErrorEnum.PERMISSION_DENIED.value)

        return decorated_function

    return wrapper


def error_handler(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except AddressValueError as a:
            data = return_response(False, ControllerErrorEnum.VALIDATION_FAILED.value)
            if "hex" in a.args[0]:
                data["message"] = "ipv6"
            elif "Octet" or "octets" in a.args[0]:
                data["message"] = "ipv4"
            else:
                data["message"] = a.args[0]
            logger.error(a)
            return data
        except ValueError as v:
            if v.args[0] == "in use":
                data = return_response(False, BaseDaoError.DATA_IN_USE.value)
                data["message"] = v.args[1]
            elif "hex_codec" in v.args[0]:
                data = return_response(
                    False, ControllerErrorEnum.VALIDATION_FAILED.value
                )
                data["message"] = "key"
            else:
                data = return_response(
                    False, ControllerErrorEnum.AUTHENTICATION_FAILED.value
                )
                data["message"] = v.args[0]
            logger.error(v)
            return data
        except ValidationError as va:
            data = return_response(False, ControllerErrorEnum.VALIDATION_FAILED.value)
            data["message"] = va.args[0]
            if va.args[0].get("tis_ips"):
                tis_ips = va.args[0].get("tis_ips")[0]
                data["message"] = "domain" if "domain" in tis_ips else "ip or domain"
            else:
                data["message"] = va.args[0]
            logger.error(va)
            return data
        except AttributeError as a:
            message = re_for_error_message(a.args[0])
            data = return_response(False, BaseDaoError.DATA_NOT_FOUND.value)
            data["message"] = message
            logger.error(a)
            return data
        except IntegrityError as i:
            status = i.orig.args[0]
            message = re_for_error_message(i.orig.args[1])
            if status == 1062:
                data = return_response(False, BaseDaoError.DATA_EXISTED.value)
                if re.search(email_regex, message):
                    data["message"] = "email"
                elif re.search(ip_regex, message):
                    data["message"] = "ip"
                else:
                    data["message"] = "name"
                return data
            elif status == 1048:
                data = return_response(False, BaseDaoError.DATA_NULL.value)
                data["message"] = message
                return data
            logger.error(i)
            return message
        except DataError as d:
            status = d.orig.args[0]
            message = re_for_error_message(d.orig.args[1])
            if status == 1406:
                data = return_response(False, BaseDaoError.DATA_TOO_LONG.value)
                data["message"] = message
                return data
            logger.error(d)
            return message
        except UnmappedInstanceError as u:
            message = re_for_error_message(u.args[0])
            data = return_response(False, BaseDaoError.DATA_NOT_FOUND.value)
            data["message"] = message
            logger.error(u)
            return data
        except Exception as e:
            logger.error(e)
            return return_response(False, "Error code")

    return decorated


def superuser_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # 檢查是否為Super user
            user = session.get("current_user")
            if not user["is_admin"]:
                raise Exception(ControllerErrorEnum.PERMISSION_DENIED.value)

        except Exception as e:
            logger.error(e, exc_info=True)
            msg = e.args[0]
            return_response(False, msg)

        return f(*args, **kwargs)

    return decorated

