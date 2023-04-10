from flask_restful import Resource
from app.auth.util.decorator import error_handler
from common.util.response_util import return_response
from app.operator_record.service.operator_record_service import add_record_to_db
from app.operator_record.service.web_url_service import get_web_url_menu

import logging

logger = logging.getLogger(__name__)


class WebUrlMenu(Resource):
    @classmethod
    @error_handler
    def get(cls):
        logger.info(f"[Resource] <{cls.__name__}> starts to fetch the menu")
        res = get_web_url_menu()
        add_record_to_db(True)
        return return_response(True, res)
