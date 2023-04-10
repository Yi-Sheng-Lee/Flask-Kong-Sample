from sqlalchemy.ext.associationproxy import association_proxy

from common.util.common_util import generate_uuid
from app import db
from datetime import datetime


class UserOperationRecord(db.Model):
    __tablename__ = "user_operation_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_company_id = db.Column(db.String(255), nullable=False)
    user_company = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_ip = db.Column(db.String(255))
    web_url = db.Column(db.String(1000))
    api_url = db.Column(db.String(1000), nullable=False)
    api_method = db.Column(db.String(32), nullable=False)
    api_action = db.Column(db.String(32), nullable=False)
    api_payload = db.Column(db.String(5000))
    message = db.Column(db.String(5000))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    company = db.relationship("Company", lazy=True)
    company_uid = association_proxy('company', 'uid')


class Api(db.Model):
    __tablename__ = "api"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1000))
    name = db.Column(db.String(100))


class WebUrl(db.Model):
    __tablename__ = "web_url"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1000))
    name = db.Column(db.String(100))
