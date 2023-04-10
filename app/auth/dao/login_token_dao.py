from common.dao.base_dao import BaseDao
from app.auth.model.models import LoginToken
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


class TokenNotFound(Exception):
    """
    Indicates that a token could not be found in the database
    """

    pass


class LoginTokenDao(BaseDao):
    """
    Table command_action_log data access
    """

    def __init__(self):
        super().__init__(LoginToken)

    @classmethod
    def get_by_jti(cls, jti):
        return LoginToken.query.filter_by(jti=jti).first()

    @classmethod
    def get_by_user_identity(cls, user_identity):
        return LoginToken.query.filter_by(user_identity=user_identity).all()

    @classmethod
    def get_by_user_identity_and_unrevoked(cls, user_identity):
        try:
            res = LoginToken.query.filter_by(
                user_identity=user_identity,
                is_revoked=0
            ).all()
        except NoResultFound:
            raise TokenNotFound("token not found {}".format(user_identity))
        return res

    @classmethod
    def get_by_user_identity_and_jti(cls, user_identity, _id):
        try:
            res = LoginToken.query.filter_by(
                jti=_id,
                user_identity=user_identity
            ).first()
        except NoResultFound:
            raise TokenNotFound("token not found {}".format(_id))
        return res

    @classmethod
    def get_by_expired_time(cls):
        now = datetime.now()
        return LoginToken.query.filter(LoginToken.expires < now).all()
