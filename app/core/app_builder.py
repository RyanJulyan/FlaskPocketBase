import os
from typing import Any, Dict

from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from plugo.services.plugin_manager import load_plugins as load_with_plugo


try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError as e:
    print(e)

from configuration.config import Config, default_config_factory

from app.core.app_factory import create_app
from app.core.database.database import db
from app.core.flask_security.init_flask_security import init_flask_security
from app.core.cors.flask_cors import init_flask_cors
from app.core.limiter.flask_limiter import init_flask_limiter
from app.core.talisman.flask_talisman import init_flask_talisman
from app.core.before_request.before_request import before_request
from app.core.context_processor.context_processor import context_processor
from app.core.health_check.view import health_check
from app.core.errorhandler.errorhandler import errorhandler
from app.core.api_factory import create_api
from app.core.health_check.rest_api import health_check_api
from app.core.flask_admin.init_flask_admin import init_flask_admin


def build_app(
    config_factory: Dict[str, Config] = {},
    extensions_directory: str = "app/extensions",
    extensions_config_path: str = "configuration/extensions_config.json",
    plugins_directory: str = "app/plugins",
    plugins_config_path: str = "configuration/plugins_config.json",
    template_folder: str = "templates",
    health_check_kwargs: Any = {},
    authorizations: Dict[str, Dict[str, str]] = {},
) -> Any:
    config_factory = {**default_config_factory, **config_factory}
    env_config_setting = os.environ.get("ENV", "default")

    config_object = config_factory[env_config_setting]()

    app = create_app(
        config_object=config_object,
        template_folder=template_folder,
    )

    app.db = db
    app.db.init_app(app=app)

    app = init_flask_security(app=app)

    app.csrf_protect = CSRFProtect(app)

    app = init_flask_cors(app=app)

    app = init_flask_limiter(app)

    app = init_flask_talisman(app)

    app.mail = Mail(app)

    if app.config["DEBUG"]:
        app.toolbar = DebugToolbarExtension(app)

    before_request(app=app)

    context_processor(app=app)

    health_check(app=app, **health_check_kwargs)

    # errorhandler(app=app)

    app = create_api(app=app, authorizations=authorizations)
    health_check_api(app=app, **health_check_kwargs)

    app = init_flask_admin(app)

    loaded_extensions = load_with_plugo(
        plugin_directory=extensions_directory,
        config_path=extensions_config_path,
        app=app,
    )

    loaded_plugins = load_with_plugo(
        plugin_directory=plugins_directory,
        config_path=plugins_config_path,
        app=app,
    )

    return app
