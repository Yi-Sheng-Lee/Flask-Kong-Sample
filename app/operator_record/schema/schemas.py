from app import ma
from ..model import models
from app.asset.schema.schemas import CompanySchema
from marshmallow import validate, validates

from common.util.common_util import (ip_regex)


class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.UserOperationRecord
        load_instance = True
        include_fk = True

    create_at = ma.DateTime("%Y-%m-%d %H:%M:%S")
    company = ma.Nested(CompanySchema, only=("uid", "name"))


class RecordFilterSchema(ma.Schema):
    start_time = ma.Str()
    end_time = ma.Str()
    status = ma.Str()
    user_name = ma.Str()
    # user_company_id = ma.Str()
    user_ip = ma.Str()
    company_uid = ma.Str()
    web_url = ma.Str()
    api_action = ma.Str()
    page = ma.Int()
    per_page = ma.Int()


class RecordDownloadFieldSchema(ma.Schema):
    start_time = ma.Str()
    end_time = ma.Str()
    status = ma.Str()
    user_name = ma.Str()
    user_company_id = ma.Str()
    user_ip = ma.Str()
    # api_method = ma.Str()
    api_action = ma.Str()


class ApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Api
        load_instance = True
        exclude = ["id"]


class WebUrlSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.WebUrl
        load_instance = True,
        exclude = ["id"]
