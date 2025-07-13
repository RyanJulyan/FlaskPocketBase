from typing import Any, Dict

from flask import Flask
from flask_restx import Api

from app.core.custom_api import CustomApi


def create_api(
    app: Any, authorizations: Dict[str, Dict[str, str]] = {}
) -> Any:
    default_authorizations = app.config["DEFAULT_AUTHORIZATIONS"]

    # Merge default and provided authorizations
    authorizations = {**default_authorizations, **authorizations}

    # Initialize API with dynamic config
    app.api = CustomApi(
        app,
        version=app.config["API_VERSION"],
        title=app.config["SITE_TITLE"] + " API",
        description=app.config["SITE_DESCRIPTION"] + " API",
        doc=app.config["SWAGGER_URL"],
        # security=app.config["API_SECURITY"],
        security=["jwt", "apikey", "token", "Bearer Auth"],
        decorators=[app.csrf_protect.exempt],
        authorizations=authorizations,
    )

    return app
