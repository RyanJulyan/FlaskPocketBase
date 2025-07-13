from typing import Any
from flask_limiter.extension import Limiter
from flask_limiter.util import get_remote_address


def init_flask_limiter(app: Any):
    app.limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config["RATELIMIT_STORAGE_URI"],
        default_limits=[app.config["RATELIMIT_DEFAULT"]],
    )

    return app
