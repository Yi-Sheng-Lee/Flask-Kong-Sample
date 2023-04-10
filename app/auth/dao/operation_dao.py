from common.dao.base_dao import BaseDao
from app.auth.model.models import Operation
from app import db


class OperationDao(BaseDao):
    """
    Table Operation data access
    """

    def __init__(self):
        super().__init__(Operation)

    def get_by_name(self, name):
        return self.get_all_by_fields(name=name).first()

    @classmethod
    def get_operations_all(cls):
        return Operation.query.order_by(Operation.id).all()


