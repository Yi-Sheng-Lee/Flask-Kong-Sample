from common.dao.base_dao import BaseDao
from app.asset.model.models import Sensor
import logging

logger = logging.getLogger(__name__)


class SensorDao(BaseDao):
    """
    Table Sensor data access
    """

    def __init__(self):
        super().__init__(Sensor)

    def get_verify_list(self, page, per_page, **req_filter):
        self.set_filters(**req_filter)

        try:
            q = Sensor.query.filter(*self.filters)
            res_data = q.paginate(page=page, per_page=per_page, error_out=False)
            res = {
                "on_page": self.curr_page if self.curr_page else 1,
                "limit": self.page_size if self.page_size else res_data.total,
                "total_pages": res_data.pages if res_data else 1,
                "total": res_data.total if res_data else 0,
                "data": res_data.items if res_data else []
            }
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            return res
