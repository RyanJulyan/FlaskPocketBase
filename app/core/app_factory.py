from typing import Any, Literal

from flask import Flask

from configuration.config import Config


def create_app(config_object: Config) -> Any:
  app = Flask(__name__)
  app.config.from_object(config_object)
  return app

