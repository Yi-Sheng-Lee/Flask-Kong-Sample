from common.dao.base_dao import BaseDao
from app.asset.model.models import DeviceGroupTopology


class DeviceGroupTopologyDao(BaseDao):
    """
    Table device group topology data access
    """

    def __init__(self):
        super().__init__(DeviceGroupTopology)
