from app import ma
from app.auth.model import models
from marshmallow import validate, validates, ValidationError
from common.util.common_util import (
    code_regex,
    ip_rough_regex,
    domain_regex,
    validate_ipv4,
    validate_ipv6,
)
import re


class LoginFieldSchema(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(
        required=True
    )


class LoginTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.LoginToken
        dump_only = ("id",)
        load_instance = True


class LoginRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.LoginRecord
        dump_only = (
            "id",
            "last_login",
        )
        include_fk = True
        load_instance = True


class UserBulkSchema(ma.Schema):
    users = ma.List(ma.Str(), required=True, validate=[validate.Length(min=1)])


class UserFieldSchema(ma.Schema):
    name = ma.Str(required=True, validate=[validate.Length(min=3)])
    nickname = ma.Str(required=True, validate=[validate.Length(min=2)])
    phone = ma.Str(required=True, validate=[validate.Length(min=1, max=10)])
    password = ma.Str(
        required=True,
        validate=[validate.Length(min=6), validate.Regexp(code_regex)],
    )
    old_password = ma.Str(
        validate=[validate.Length(min=6), validate.Regexp(code_regex)]
    )
    new_password = ma.Str(
        validate=[validate.Length(min=6), validate.Regexp(code_regex)]
    )
    email = ma.Email(required=True)
    role_uid = ma.Str(required=True)
    company_id = ma.Int(default=0, missing=0)
    is_admin = ma.Int(default=0, missing=0)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        load_only = ("password",)
        exclude = (
            "id",
            "is_delete",
            "create_at",
            "update_at",
            "roles_id",
        )
        include_fk = True
        load_instance = True

    role_id = ma.auto_field("roles_id")
    company_uid = ma.Str()
    company_name = ma.Str()
    is_admin_company = ma.Int()
    role_uid = ma.Str()
    role_name = ma.Str()


class RolePermissionFieldSchema(ma.Schema):
    p_id = ma.Int(required=True)
    o_id = ma.Int(required=True)


class RolePermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.RolePermission
        dump_only = ("id",)
        exclude = (
            "permissions_id",
            "operations_id",
            "is_revoked",
            "create_at",
            "update_at",
        )
        include_fk = True
        load_instance = True

    p_id = ma.auto_field("permissions_id")
    o_id = ma.auto_field("operations_id")


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Permission
        include_fk = True
        load_instance = True


class OperationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Operation
        include_fk = True
        load_instance = True


class RoleBulkSchema(ma.Schema):
    roles = ma.List(ma.Str(), required=True, validate=[validate.Length(min=1)])


class RoleFieldSchema(ma.Schema):
    name = ma.Str(required=True, validate=[validate.Length(min=3)])
    description = ma.Str(required=True)
    auth = ma.List(
        ma.Dict(keys=ma.Str(), values=ma.Int()),
        required=True,
        validate=[validate.Length(min=1)],
    )


class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = models.Role
        dump_only = ("id",)
        exclude = (
            "create_at",
            "update_at",
        )
        load_instance = True
    company_uid = ma.Str()
    company_name = ma.Str()
