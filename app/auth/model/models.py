from sqlalchemy.ext.associationproxy import association_proxy
from app import db
from common.util.common_util import generate_uuid
from datetime import datetime

class LoginToken(db.Model):
    __tablename__ = "login_tokens"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    is_revoked = db.Column(db.Integer, nullable=False, default=0)
    expires = db.Column(db.DateTime, nullable=False)

class LoginRecord(db.Model):
    __tablename__ = "login_records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(5000), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(50), nullable=False, default=generate_uuid)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    name = db.Column(db.String(250), nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Integer, default=0)
    is_delete = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    roles_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at = db.Column(
        db.DateTime,
        onupdate=datetime.now,
        default=datetime.now,
        nullable=False,
    )
    login_records = db.relationship("LoginRecord", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    company = db.relationship("Company", lazy=True, backref='user')
    company_uid = association_proxy('company', 'uid')
    company_name = association_proxy('company', 'name')
    is_admin_company = association_proxy('company', 'is_admin')
    role_uid = association_proxy('role', 'uid')
    role_name = association_proxy('role', 'name')

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(50), nullable=False, default=generate_uuid)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, server_default='1', default=1)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at = db.Column(
        db.DateTime,
        onupdate=datetime.now,
        default=datetime.now,
        nullable=False,
    )
    permissions = db.relationship("RolePermission", backref="permission", lazy=True)
    users = db.relationship("User", backref="role", lazy=True)
    company = db.relationship("Company", backref="role", lazy=True)
    company_uid = association_proxy('company', 'uid')
    company_name = association_proxy('company', 'name')


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    enable = db.Column(db.Integer, default=0, nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)

class Operation(db.Model):
    __tablename__ = "operations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class RolePermission(db.Model):
    __tablename__ = "roles_permissions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roles_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    permissions_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), nullable=False
    )
    operations_id = db.Column(
        db.Integer, db.ForeignKey("operations.id"), nullable=False
    )
    is_revoked = db.Column(db.Integer, default=0, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at = db.Column(
        db.DateTime,
        onupdate=datetime.now,
        default=datetime.now,
        nullable=False,
    )