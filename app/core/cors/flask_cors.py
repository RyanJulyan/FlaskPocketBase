from typing import Any
from flask_cors import CORS


def init_flask_cors(app: Any):
    app.cors = CORS(
        app=app,
        resources=app.config["CORS_RESOURCES"],
        supports_credentials=app.config["CORS_SUPPORTS_CREDENTIALS"],
        allow_headers=app.config["CORS_ALLOW_HEADERS"],
        methods=app.config["CORS_METHODS"],
        max_age=app.config["CORS_MAX_AGE"],
    )

    return app
