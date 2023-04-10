"""
Utility Functions
"""
from ipaddress import IPv4Address, IPv6Address
import codecs
from datetime import datetime
import uuid


email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#password 名稱更換 解高風險弱掃
code_regex = "^(?=.*[a-zA-Z])(?=.*\d)\S{6,}$"
ip_rough_regex = "\d{1,3}.\d{1,3}"
ip_regex = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
ip_domain_regex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"
domain_regex = "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"


def generate_uuid():
    return str(uuid.uuid4())


def to_dict(res):
    """
    Flask-SQLAlchemy result model convert to dict function
    """
    if type(res) == list:
        return [log.to_dict() for log in res]
    else:
        return res.to_dict()


def key_exist_and_not_empty(dict_obj, key):
    """
    Check dict object key exist and value is not empty.
    :param dict_obj:
    :param key:
    :return:
    """
    return True if key in dict_obj.keys() and dict_obj[key] else False


# def decrypt(string, key):
#     cl = Blowfish.new(key, Blowfish.MODE_ECB)
#     cipher_text = codecs.decode(string, "hex_codec")
#     code = cl.decrypt(cipher_text)
#     return code.decode("utf-8").strip()


def validate_ipv4(ip):
    return IPv4Address(ip)


def validate_ipv6(ip):
    return IPv6Address(ip)


def convert_list_of_obj_to_dict(objs):
    return {obj.key: obj.value for obj in objs}


def diff_days(start_time, end_time):
    start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    day_diff = (end_date - start_date).days
    return day_diff


def diff_datetime(start_time, end_time, util):
    if len(start_time) == 10:
        start_time = f"{start_time} 00:00:00"

    if len(end_time) == 10:
        end_time = f"{end_time} 00:00:00"

    start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    diff = 0
    if util == 'H':
        diff = ((end_date - start_date).total_seconds() / 3600) + 1
    elif util == 'D':
        diff = (end_date - start_date).days + 1
    elif util == 'M':
        diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

    return int(diff)


def statistic_datetime_util(start_time, end_time):
    days = diff_days(start_time, end_time)
    if days == 0:
        util = 'H'
    elif days > 31:
        util = 'M'
    else:
        util = 'D'
    return util