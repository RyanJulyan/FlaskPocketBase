import os
from typing import Any, Dict

from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from app.core.flask_security.init_flask_security import init_flask_security

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError as e:
    print(e)

from configuration.config import Config, default_config_factory

from app.core.app_factory import create_app
from app.core.before_request.before_request import before_request
from app.core.context_processor.context_processor import context_processor
from app.core.health_check.view import health_check
from app.core.errorhandler.errorhandler import errorhandler
from app.core.database.database import db
from app.core.flask_admin.init_flask_admin import init_flask_admin
from app.extensions.register_extensions import (
    DEFAULT_EXTENSIONS_DIRECTORY,
    register_extensions,
)
from app.plugins.register_plugins import (
    DEFAULT_PLUGINS_DIRECTORY,
    register_plugins,
)


def build_app(
    config_factory: Dict[str, Config] = {},
    extensions_directory: str = DEFAULT_EXTENSIONS_DIRECTORY,
    plugins_directory: str = DEFAULT_PLUGINS_DIRECTORY,
    template_folder="templates",
    health_check_kwargs: Any = {},
) -> Any:
    config_factory = {**default_config_factory, **config_factory}
    flask_env = os.environ.get("FLASK_ENV", "default")

    app = create_app(
        config_object=config_factory[flask_env],
        template_folder=template_folder,
    )

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    app.csrf_protect = CSRFProtect(app)

    if app.config["DEBUG"]:
        app.toolbar = DebugToolbarExtension(app)

    app.db = db.init_app(app)

    app.security = init_flask_security(app=app)

    before_request(app)

    context_processor(app)

    health_check(app, **health_check_kwargs)

    errorhandler(app)

    app.admin = init_flask_admin(app)

    register_extensions(app=app, extensions_directory=extensions_directory)

    register_plugins(app=app, plugins_directory=plugins_directory)

    return app
