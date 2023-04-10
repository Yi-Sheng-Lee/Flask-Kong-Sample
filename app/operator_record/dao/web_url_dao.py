from sqlalchemy import desc, asc
from common.dao.base_dao import BaseDao
from app.operator_record.model.models import WebUrl
import logging

logger = logging.getLogger(__name__)


class WebUrlDao(BaseDao):
    def __init__(self):
        super().__init__(WebUrl)

    # def get_one_by_fields(self, **kwargs):
    #     self.set_filter_field_like(**kwargs)
    #     q = self._model.query.filter(*self.filters)
    #     res = q.first()
    #     return res

    def get_by_url(self, _url):
        return super().get_all_by_fields(url=_url)


