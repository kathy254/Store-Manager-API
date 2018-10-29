from flask import Flask
import json
from flask_restplus import Api
from jsonschema import validate

from .api.v1 import app_v1
from instance.config import app_config

from flask_bcrypt import Bcrypt


def create_app(config):
    app = Flask(__name__)
    app.register_blueprint(app_v1)
    app.config.from_object(app_config[config])
    return app