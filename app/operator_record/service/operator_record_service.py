from flask_jwt_extended import decode_token, get_jwt_claims
from flask import request, send_file, current_app
from app.auth.dao.user_dao import UserDao
from app.operator_record.dao.operator_record_dao import UserOperationRecordDao
from app.operator_record.dao.api_dao import ApiDao
from app.operator_record.dao.web_url_dao import WebUrlDao
from app.auth.schema.schemas import UserSchema
from app.operator_record.schema.schemas import RecordFilterSchema, RecordSchema, RecordDownloadFieldSchema, ApiSchema, WebUrlSchema
from app.operator_record.model.models import UserOperationRecord


import os
import json
import logging
import csv
import re
from datetime import datetime

logger = logging.getLogger(__name__)


def add_record_to_db(status, action='VIEW', error=''):
    web_url = request.headers.get("M-URL")

    # 判別 web_url 是否存在且是不是含有 mssp/admin 字眼
    if not web_url:
        return
    if "mssp/admin" not in web_url:
        return

    auth = request.headers.get("Authorization")
    identity = ''
    if auth:
        auth = auth.replace('Bearer ', '')
    if not auth == 'null' and not auth == 'undefined' and auth is not None:
        token = auth.replace("Bearer ", "")
        identity = decode_token(token, allow_expired=True)["identity"]

    users = []
    user_info = {}

    if True if identity else False:
        users = UserDao().get_all_by_fields(uid=identity)
    elif request.path.replace('/api/1.0/', '/') == '/login':
        user_data = request.get_json()
        users = UserDao().get_all_by_fields(name=user_data['username'])

    if len(users) > 0:
        for user in users:
            user_info = UserSchema().dump(user)

    record = UserOperationRecord()
    record.status = 1 if status else 0
    record.user_id = user_info["uid"] if len(users) > 0 else ''
    record.user_name = user_info["name"] if len(users) > 0 else ''
    record.user_company_id = user_info["company_uid"] if len(users) > 0 else ''
    record.user_company = user_info["company_name"] if len(users) > 0 else ''
    record.company_id = user_info["company_id"]
    record.user_ip = request.remote_addr

    try:
        _ip = request.headers.get("X-Real-IP")
        if _ip is not None:
            record.user_ip = _ip
    except Exception as e:
        print(e)

    if web_url != "None":
        url = web_url.replace("/mssp/admin/#/", "/").split('?')[0].split('://')[1].split('/', 1)[1]
        for v in ["/add", "/edit", "/batch-add"]:
            url = url.replace(v, '')
        web_url = f'/{url}'

    record.web_url = web_url or ""
    record.api_url = request.path.replace('/api/1.0/', '/').replace('/taxii2.1/', '/')
    record.api_method = request.method
    record.api_action = action
    record.message = str(error) if error else "SUCCESS"

    if request.method == "GET":
        record.api_payload = request.query_string.decode('utf-8')
    else:
        payload = request.get_json()
        if payload:
            if isinstance(payload, dict):
                payload = dict(payload)
                if "password" in payload.keys() or "old_password" in payload.keys():
                    payload["password"] = "******"
                payload = json.dumps(payload, ensure_ascii=False)
            elif isinstance(payload, list):
                payload = str(payload)

        record.api_payload = '' if (payload == 'null' or not payload) else payload

    try:
        write_record_to_local(record)
        UserOperationRecordDao().add(record)
    except Exception as e:
        logging.error(e)


def get_record_by_filter(**kwargs):
    try:
        filters = RecordFilterSchema().load(kwargs)
        page = filters.get("page", 1)
        per_page = filters.get("per_page", 10)
        record_dao = UserOperationRecordDao()
        record_dao.set_pager(page, per_page)
        record_dao.set_order_by(["id"], "DESC")

        claims = get_jwt_claims()
        company_id = claims["company_id"]

        res = record_dao.get_all_by_fields(**filters) if company_id == 1 else record_dao.get_all_by_fields(**filters, company_id=company_id)

        tmp_data = []
        for record in RecordSchema(many=True).dump(res["data"]):

            re_id = re.compile('/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
            web_url = re_id.sub('', record["web_url"])
            re_id = re.compile('/[0-9a-z]{24}$')
            web_url = re_id.sub('', web_url)

            tmp_data.append({
                # "id": record["id"],
                "status": record["status"],
                "create_at": record["create_at"],
                "url": record_url(web_url),
                "name": record["user_name"],
                "ip": record["user_ip"],
                "action": record["api_action"],
                "obj": record_object(record),
                "company": record["company"]
            })
        res["data"] = tmp_data
    except Exception as e:
        logger.error(e, exc_info=True)
    else:
        return res


def record_url(url):
    # 針對 incident, accident 有 /SOC- 字眼做過濾
    url_split = url.split("/SOC-")[0]
    web_url = WebUrlDao().get_by_url(url_split)
    url_dump = WebUrlSchema(many=True).dump(web_url)
    return url_dump[0]["name"] if len(url_dump) > 0 else ""


def record_object(record):
    auth = ["LOGIN", "REFRESH", "LOGOUT", "SEND_MAIL"]
    api_dao = ApiDao()

    re_id = re.compile('/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    url = re_id.sub('', record["api_url"])
    re_id = re.compile('/[0-9a-z]{24}$')
    url = re_id.sub('', url)
    url = url.split("/SOC-")[0]
    url = url.split("/city/menu")[0]
    url = url.split("/zip/menu")[0]
    url_name = ApiSchema(many=True).dump(api_dao.get_by_url(url))
    if record["api_action"] in auth or len(url_name) == 0:
        return ''
    elif url == '/accidents' and record["api_action"] == 'DELETE':
        return dict(url_name[1])["name"]
    else:
        return dict(url_name[0])["name"]


def get_record_csv(**kwargs):
    filters = RecordDownloadFieldSchema().load(kwargs)
    record_dao = UserOperationRecordDao()
    record_list = []
    res = record_dao.get_all_by_fields(**filters)
    res = RecordSchema(many=True).dump(res)
    i = 1
    for record in res:
        record_list.append({
            'index': i,
            'status': "成功" if record["status"] == 0 else "失敗",
            'create_at': record["create_at"],
            'user_name': record["user_name"],
            'user_company': record["user_company"],
            'user_ip': record["user_ip"],
            'web_url': record["web_url"],
            'api_url': record["api_url"],
            'api_method': record["api_method"],
            'api_action': record["api_action"],
            'api_payload': record["api_payload"],
            'message': record["message"]
        })
        i = i + 1

    keys = record_list[0].keys()
    filename = '/tmp/operation.csv'

    with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(record_list)

    return send_file(filename, attachment_filename='operation_record.csv', as_attachment=True)


def write_record_to_local(records):
    record = records
    record.create_at = datetime.now()
    now = datetime.today().strftime("%Y_%m")

    path = f"{current_app.config['RECORD_FILE_PATH']}record_{now}.csv"
    data = RecordSchema().dump(record)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    file_exist = True if os.path.isfile(path) else False

    with open(path, 'a', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=data.keys())
        if not file_exist:
            dict_writer.writeheader()
        dict_writer.writerows([data])

        output_file.close()
