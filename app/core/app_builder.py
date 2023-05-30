import os
from typing import Any, Dict

from flask import Flask

from configuration.config import Config, default_config_factory
from app.core.app_factory import create_app
from app.extensions.register_extensions import (
    DEFAULT_EXTENSIONS_DIRECTORY,
    register_extensions,
)
from app.plugins.register_plugins import (
    DEFAULT_PLUGINS_DIRECTORY,
    register_plugins,
)


def build_app(
    config_factory: Dict[str, Config],
    extensions_directory: str = DEFAULT_EXTENSIONS_DIRECTORY,
    plugins_directory: str = DEFAULT_PLUGINS_DIRECTORY,
) -> Any:
    config_factory = {**default_config_factory, **config_factory}
    flask_env = os.environ.get("FLASK_ENV", "default")

    app = create_app(config_object=config_factory[flask_env])

    register_extensions(app=app, extensions_directory=extensions_directory)

    register_plugins(app=app, plugins_directory=plugins_directory)

    return app
