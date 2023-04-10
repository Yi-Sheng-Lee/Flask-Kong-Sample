from flask import Blueprint
from flask_restful import Api

from .controller.login_controller import Login, LoginRefresh, Logout
from .controller.role_controller import PermissionsMenu, RolesMenu, Roles, Role
from .controller.user_controller import UsersMenu, Users, User, UserProfile


def create_module():
    bp = Blueprint('auth', __name__)
    api = Api(bp)
    # Login/Logout
    api.add_resource(LoginRefresh, '/api/1.0/login/refresh')
    api.add_resource(Login, '/api/1.0/login')
    api.add_resource(Logout, '/api/1.0/logout')

    # User
    api.add_resource(UsersMenu, "/api/1.0/users/menu")
    api.add_resource(Users, "/api/1.0/users")
    api.add_resource(User, "/api/1.0/user/<string:user_uid>", "/api/1.0/user")
    api.add_resource(UserProfile, "/api/1.0/user/profile")

    # Permission & roles
    api.add_resource(PermissionsMenu, "/api/1.0/permissions/menu")
    api.add_resource(RolesMenu, "/api/1.0/roles/menu")
    api.add_resource(Roles, "/api/1.0/roles")
    api.add_resource(Role, "/api/1.0/role/<string:uid>", "/api/1.0/role")
    return bp
