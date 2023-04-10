from common.dao.base_dao import BaseDao
from app.operator_record.model.models import Api
import logging

logger = logging.getLogger(__name__)


class ApiDao(BaseDao):
    def __init__(self):
        super().__init__(Api)

    def get_by_url(self, _url):
        return super().get_all_by_fields(url=_url)
