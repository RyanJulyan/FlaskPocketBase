from typing import Any

from flask import Flask

from configuration.config import Config


def create_app(config_object: Config, template_folder="templates") -> Any:
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_object(config_object)
    return app
