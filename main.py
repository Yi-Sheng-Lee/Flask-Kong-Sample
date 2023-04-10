import flask_restful as restful
from app import create_app
import os
import importlib
import logging

app = create_app()
api = restful.Api(app)
logger = logging.getLogger(__name__)

# router
# Auto register blueprint
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
apps = [app for app in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, app)) and not app.startswith("__")]
for app_name in apps:
    app_path = package_path = '.'.join(['app', app_name])
    app_module = importlib.import_module(app_path)
    if hasattr(app_module, "create_module"):
        logger.debug(f"Load app {app_path}.")
        app.register_blueprint(app_module.create_module())

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
    # socketio.run(app=app, host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
