from sqlalchemy import desc, asc, func

from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging
from flask_jwt_extended import get_jwt_claims
logger = logging.getLogger(__name__)


class BaseDao:
    """
    共用Mysql Database 存取類別

    Attributes
    ----------
    _model: SQLAlchemy model
        被存取之 model
    pager: boolean
        是否啟用分頁查詢
    curr_page: int
        分頁查詢頁碼, 需搭配 pager=True 才會啟動
    page_size: int
        分頁查詢單頁筆數, 需搭配 pager=True 才會啟動
    order_by: str
        查詢結果排序，預設 ASC, 可使用 ASC, DESC等方式
    order_by_fields: list[str]
        查詢結果排序欄位
    req_user: dict
        存取 user data
    claims: dict
        JWT 資訊，內容為登入資訊
    filters: list[SQLAlchemy filter]
        過濾條件，List 內容為 SQLAlchemy 欄位運算式 ex: model.field == value
    """

    def __init__(self, model, user_auth=False):
        """
        建構式
        :param model: SQLAlchemy access model
        :param user_auth: 是否要使用過濾 create_user
        """
        self._model = model
        self.pager = False
        self.curr_page = 1
        self.page_size = None
        self.order_by = "ASC"
        self.order_by_fields = []
        self.req_user = None
        self.claims = None
        self.filters = []
        self.__init_claims()
        self.user_auth = user_auth
        self.db = db

    def __init_claims(self):
        try:
            self.claims = get_jwt_claims()
            if self.claims:
                from app.auth.model.models import User
                self.req_user = User.query.filter_by(name=self.claims["user"]).first()
        except:
            logger.info(f"No claims info")

    def set_pager(self, curr_page, page_size=None):
        self.pager = True
        self.curr_page = curr_page
        self.page_size = page_size

    def disable_pager(self):
        self.pager = False
        self.curr_page = 1
        self.page_size = None

    def set_order_by(self, order_by_fields=[], order_by="ASC"):
        self.order_by = order_by
        self.order_by_fields = order_by_fields

    def reset_order_by(self):
        self.order_by = "ASC"
        self.order_by_fields = []

    def get_by_id(self, _id):
        return self._model.query.filter_by(id=_id).first()

    def get_by_uid(self, _uid):
        return self._model.query.filter_by(uid=_uid).first()

    def get_by_name(self, _name):
        if not hasattr(self._model, 'name'):
            return None

        return self._model.query.filter_by(name=_name).first()

    @staticmethod
    def _dt_formatter(_datetime):
        """
        轉換為DB使用時間, Format: %Y-%m-%d %H:%M:%S
        :param _datetime:
        :return:
        """
        dt_format = "%Y-%m-%d %H:%M:%S"
        return func.date_format(_datetime, dt_format)

    def set_filters(self, **kwargs):
        """
        設定過濾條件, 預設皆為 field == value

        權限設定:
        self.auth 表示需要限制model.company_id = login user company.id
        self.user_auth 表示需要限制model.create_user = login user

        建立時間區間計算:
        kwargs內包含 start_time 會帶入 model.create_at >= start_time
        kwargs內包含 end_time 會帶入 model.create_at <= end_time

        :param kwargs:
        :return:
        """

        if self.claims:
            # 判斷是否為總公司
            if not self.claims["is_admin_company"] and hasattr(self._model, "company_id"):
                logger.info(f"Set company auth company_id: {self.claims.get('company_id')}")
                self.filters.append(self._model.company_id == self.claims.get("company_id"))

            # 判斷是否要受到資料擁有者限制
            if self.user_auth and not self.claims["is_admin"] and hasattr(self._model, "create_user"):
                logger.info(f"Set user auth user: {self.claims.get('user')}")
                self.filters.append(self._model.create_user == self.claims.get("user"))

        for key, value in kwargs.items():
            if value == '':
                continue

            # 判斷計算時間區間
            if key == 'start_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at >= value)
                continue

            if key == 'end_time' and hasattr(self._model, 'create_at'):
                self.filters.append(self._model.create_at <= value)
                continue

            if hasattr(self._model, key):
                self.set_filter_field_eq(key, value)

    def set_filter_field_eq(self, field_name, value):
        if not hasattr(self._model, field_name):
            logger.info(f"Field {field_name} not exist, skip this field.")
            return

        field = getattr(self._model, field_name)
        self.filters.append(field == value)

    def set_filter_field_like(self, field_name, value):
        if not hasattr(self._model, field_name):
            logger.info(f"Field {field_name} not exist, skip this field.")
            return

        field = getattr(self._model, field_name)
        self.filters.append(field.like("%%%s%%" % value))

    def get_one_by_fields(self, **kwargs):
        self.set_filters(**kwargs)
        q = self._model.query.filter(*self.filters)
        return q.first()

    def get_all_by_fields(self, **kwargs):

        self.set_filters(**kwargs)
        q = self._model.query.filter(*self.filters)

        if self.order_by_fields:
            test = []
            order_by_func = asc if self.order_by == "ASC" else desc
            for field in self.order_by_fields:
                test.append(order_by_func(field))
            q = q.order_by(*test)
            # q = q.order_by(order_by_func(*self.order_by_fields))
        else:
            # 預設 create_at 正序
            if hasattr(self._model, 'create_at'):
                self.order_by_fields.append('create_at')

        if self.pager:
            res_data = q.paginate(page=self.curr_page, per_page=self.page_size, error_out=False)
            res = {
                "on_page": self.curr_page if self.curr_page else 1,
                "limit": self.page_size if self.page_size else res_data.total,
                "total_pages": res_data.pages if res_data else 1,
                "total": res_data.total if res_data else 0,
                "data": res_data.items if res_data else []
            }
        else:
            res = q.all()

        return res

    def get_all_without_uid(self, uid, **kwargs):
        self.set_filters(**kwargs)
        self.filters.append(self._model.uid != uid)
        return self._model.query.filter(*self.filters).all()

    def truncate_table(self, table):
        db.session.execute('SET FOREIGN_KEY_CHECKS = 0;')
        db.session.execute(f"TRUNCATE `{table}`;")
        db.session.execute('SET FOREIGN_KEY_CHECKS = 1;')
        return self.__session_commit()

    def add(self, model, set_req_user=False):
        if hasattr(model, 'company_id') and not model.company_id:
            model.company_id = self.claims['company_id']
        if hasattr(model, 'user_id') and self.req_user and set_req_user:
            model.user_id = self.req_user.id
        if hasattr(model, 'create_user'):
            model.create_user = self.claims['user'] if self.claims and 'user' in self.claims.keys() else 'system'
        if hasattr(model, 'update_user'):
            model.update_user = self.claims['user'] if self.claims and 'user' in self.claims.keys() else 'system'
        db.session.add(model)
        return self.__session_commit()

    def add_all(self, *model):
        db.session.add_all(*model)
        return self.__session_commit()

    def update(self, model):
        if hasattr(model, 'update_user'):
            model.update_user = self.claims['user'] if self.claims and 'user' in self.claims.keys() else 'system'
        return self.__session_commit()

    def delete(self, model):
        db.session.delete(model)
        return self.__session_commit()

    def commit(self):
        return self.__session_commit()

    @classmethod
    def __session_commit(cls):
        try:
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(str(e))
            raise
