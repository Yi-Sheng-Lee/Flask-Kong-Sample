import geoip2.database
from geoip2.errors import AddressNotFoundError
import logging
from common.enum.code_enum import CountryCode
import os
import sys
sys.path.append(os.getcwd())

logger = logging.getLogger(__name__)


def get_ipV4_country_code(ip):
    """
    Get IP V4 country iso code
    :param ip: IPV4 string
    :return:
    """

    try:
        if ip.startswith("192.") or ip.startswith("172.") or ip.startswith("10."):
            logger.info(f"{ip} is internal IP Address")
            return "ND"
        geoip2_db_path = os.path.join(os.getcwd(), 'app/static/lib/geoip2/GeoLite2-City.mmdb')
        with geoip2.database.Reader(geoip2_db_path) as reader:
            response = reader.city(ip)
            code = response.country.iso_code
            return code
    except AddressNotFoundError:
        logger.info(f"{ip} address not found in geoip2 database.")
        return CountryCode.UNKNOWN.value
    except Exception as e:
        logger.error(e, exc_info=True)
        return CountryCode.UNKNOWN.value


if __name__ == '__main__':
    import pymysql

    DB_USER = os.getenv("DB_USER") or "msspmgr"
    DB_HOST = os.getenv("DB_HOST") or "192.168.69.194"
    DB_DB = os.getenv("DB_DB") or "mssp"
    DB_PORT = os.getenv("DB_PORT") or 5005
    DB_PB = 'billows12345'

    conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PB, db=DB_DB,
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, src_ip, dst_ip FROM incidents")
    try:
        incidents = cursor.fetchall()
        for incident in incidents:
            id = incident.get("id")
            src_ip = incident.get('src_ip')
            dst_ip = incident.get('dst_ip')
            src_country = get_ipV4_country_code(src_ip)
            dst_country = get_ipV4_country_code(dst_ip)

            update_data = []
            if src_country != "ND":
                update_data.append(f"src_country = '{src_country}'")
            if dst_country != "ND":
                update_data.append(f"dst_country = '{dst_country}'")

            if update_data:
                update_fields = ", ".join(update_data)
                sql = f"UPDATE incidents SET {update_fields} WHERE id = {id}"
                cursor.execute(sql)
                conn.commit()
                print(sql)

    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        cursor.close()
        conn.close()