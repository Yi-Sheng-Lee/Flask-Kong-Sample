from flask_jwt_extended import get_jwt_claims
from marshmallow import INCLUDE

from app.asset.dao.device_group_dao import DeviceGroupDao
from app.asset.model.models import DeviceGroup
from app.asset.dao.company_dao import CompanyDao
from app.auth.dao.user_dao import UserDao
# from app.data_migrate.service.api_token_service import init_company_api_tokens_data
# from app.system.dao.company_config_dao import CompanyConfigDao
from common.enum.code_enum import DeviceGroupType
from common.enum.service_enum import ServiceError
from app.asset.model.models import Company
from app.asset.schema.schemas import CompanySchema, CompanyInputFormSchema
from app.auth.service.role_service import init_company_admin_role
from app.auth.service.user_service import add_user_to_db
import logging
logger = logging.getLogger(__name__)


def get_company(uid):
    company = CompanyDao().get_one_by_fields(uid=uid)
    return CompanySchema().dump(company)


def get_company_kv_list():
    claims = get_jwt_claims()
    company_id = claims["company_id"]
    companies = CompanyDao().get_all_by_fields(is_revoke=0) if company_id == 1 else CompanyDao().get_all_by_fields(is_revoke=0, id=company_id)
    res = [{"uid": company.uid, "name": company.name} for company in companies]
    return res


def get_company_by_filter(**kwargs):
    company_dao = CompanyDao()
    for k, v in kwargs.items():
        company_dao.set_filter_field_like(k, v)
    companies = company_dao.get_all_by_fields()
    schema = CompanySchema(exclude=("create_user", "update_user"))
    res = schema.dump(companies, many=True)
    return res


def add_company(**kwargs):
    claims = get_jwt_claims()
    company_id = claims["company_id"] if "company_id" in claims.keys() else 0
    form_data = CompanyInputFormSchema(unknown=INCLUDE).load(kwargs)
    company = Company()
    parent_company = CompanyDao().get_by_id(company_id)

    # check name exist in company
    if CompanyDao().get_all_by_fields(name=form_data.get("name")):
        logger.error(f'Create company failed CODE: {ServiceError.NAME_DUPLICATE.value}')
        raise Exception(ServiceError.NAME_DUPLICATE.value)

    # check tax_id exist
    if CompanyDao().get_all_by_fields(tax_id=form_data.get("tax_id")):
        logger.error(f'Create company failed CODE: {ServiceError.COMPANY_TAX_ID_DUPLICATE.value}')
        raise Exception(ServiceError.COMPANY_TAX_ID_DUPLICATE.value)

    # check user id exist
    admin_user_data = form_data.get('admin_user')
    if UserDao().get_by_name(admin_user_data.get('name')):
        logger.error(f'Create company failed CODE: {ServiceError.USERNAME_EXIST.value}')
        raise Exception(ServiceError.USERNAME_EXIST.value)

    # Add company
    company_dao = CompanyDao()
    company.pid = parent_company.id
    company.name = form_data.get('name')
    company.contact = form_data.get('contact')
    company.contact_tel = form_data.get('contact_tel')
    company.contact_email = form_data.get('contact_email')
    company.country_code = form_data.get('country_code')
    company.city_code = form_data.get('city_code')
    company.zip_code = form_data.get('zip_code')
    company.address = form_data.get('address')
    company.tax_id = form_data.get('tax_id')
    company.description = form_data.get('description')
    company_dao.add(company)

    # Init Admin Role
    admin_role = init_company_admin_role(company.id)

    # Add user
    user = add_user_to_db(
        name=admin_user_data.get('name'),
        nickname=admin_user_data.get('name'),
        email=admin_user_data.get('email'),
        phone=admin_user_data.get('phone'),
        password=admin_user_data.get('password'),
        role_uid=admin_role.uid,
        company_id=company.id,
        is_admin=1
    )

    # init default device group
    device_group = DeviceGroup()
    device_group.company_id = company.id
    device_group.name = "Default Group"
    device_group.description = "Default Group"
    device_group.sort = 0
    device_group.type = DeviceGroupType.IT.value
    device_group.is_default = 1
    DeviceGroupDao().add(device_group)

    # init default api_token data
    # init_company_api_tokens_data(company.id)

    # init default company config data
    init_company_config(company.id)

    company = CompanyDao().get_one_by_fields(id=company.id)
    return CompanySchema().dump(company)


def update_company(uid, **kwargs):
    schema = CompanySchema()
    company_dao = CompanyDao()
    company = schema.load(kwargs, instance=company_dao.get_one_by_fields(uid=uid))

    # check name exist in company
    if company_dao.get_all_without_uid(uid, name=company.name):
        logger.error(f'Update company failed CODE: {ServiceError.NAME_DUPLICATE.value}')
        raise Exception(ServiceError.DEVICE_EXIST_IN_SENSOR.value)

    # check tax_id exist
    if company_dao.get_all_without_uid(uid, tax_id=company.tax_id):
        logger.error(f'Create company failed CODE: {ServiceError.COMPANY_TAX_ID_DUPLICATE.value}')
        raise Exception(ServiceError.COMPANY_TAX_ID_DUPLICATE.value)

    company_dao.update(company)
    return schema.dump(company)


def delete_company(uids):
    res = []
    for uid in uids:
        company = CompanyDao().get_one_by_fields(uid=uid)
        if company:
            company.is_revoke = 1
            CompanyDao().update(company)
            res.append(uid)
    return res


def active_company(uids):
    res = []
    for uid in uids:
        company = CompanyDao().get_one_by_fields(uid=uid)
        if company:
            company.is_revoke = 0
            CompanyDao().update(company)
            res.append(uid)
    return res


def init_company_config(company_id):
    organization = {
        "org_name": "",
        "org_contact": "",
        "org_tel": "",
        "org_email": "",
        "org_submit_target": "2",
        "org_en_name": "",
        "soc_name": "",
        "org_no": ""
    }

    # Organization
    # for key, value in organization.items():
    #     CompanyConfigDao().add_group_config(company_id, key, value, "organization")

    # OTX Token
    # CompanyConfigDao().add_group_config(company_id, "otx_token", "", "license")



