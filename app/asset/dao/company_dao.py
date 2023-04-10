from common.dao.base_dao import BaseDao
from app.asset.model.models import Company


class CompanyDao(BaseDao):
    """
    Table Company data access
    """

    def __init__(self):
        super().__init__(Company)
