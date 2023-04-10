from common.dao.base_dao import BaseDao
from app.asset.model.models import DeviceGroup
import logging

logger = logging.getLogger(__name__)


class DeviceGroupDao(BaseDao):
    """
    Table device group data access
    """

    def __init__(self):
        super().__init__(DeviceGroup)

