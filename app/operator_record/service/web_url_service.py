from app.operator_record.dao.web_url_dao import WebUrlDao
from app.operator_record.schema.schemas import WebUrlSchema

import logging

logger = logging.getLogger(__name__)


def get_web_url_menu():
    try:
        web_url_dao = WebUrlDao()
        web_url_menu_schema = WebUrlSchema()
        return [web_url_menu_schema.dump(url) for url in web_url_dao.get_all_by_fields()]
    except Exception as e:
        logger.error(e)
