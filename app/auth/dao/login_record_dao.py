from common.dao.base_dao import BaseDao
from app.auth.model.models import LoginRecord


class LoginRecordDao(BaseDao):
    """
    Table Company data access
    """

    def __init__(self):
        super().__init__(LoginRecord)

    def get_by_user_id(self, user_id):
        return self.get_all_by_fields(user_id=user_id).all()
