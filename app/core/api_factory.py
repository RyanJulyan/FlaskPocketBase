from typing import Any, Dict

from flask import Flask
from flask_restx import Api

from configuration.config import Config


def create_api(
    app: Any, authorizations: Dict[str, Dict[str, str]] = {}
) -> Any:
    default_authorizations = {
        "jwt": {
            "type": "bearer Token",
            "in": "header",
            "name": "JWTAuthorization",
        },
    }

    authorizations = {**default_authorizations, **authorizations}

    api = Api(
        app,
        version="1.0.0",
        title=app.config["SITE_TITLE"] + " API",
        description=app.config["SITE_DESCRIPTION"] + " API",
        base_url="/api",  # this did not work when set so moved to docs
        doc=app.config["SWAGGER_URL"],
        security=["jwt", "mandate"],
        decorators=[app.csrf_protect.exempt],
        authorizations=authorizations,
    )

    return api
