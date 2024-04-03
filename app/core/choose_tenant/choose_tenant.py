from typing import Any

from flask import g, request

from app.core.database.database import db


def choose_tenant(app: Any) -> None:
    g.organization = "default"

    host = request.environ.get("HTTP_HOST").split(".")

    if "organization" in request.args:
        g.organization = request.args["organization"]
        app.logger.info("Organisation changed: " + g.organization)
    elif len(host) == 3 and host[0] != "www":
        g.organization = host[0]
        app.logger.info("Organisation changed: " + g.organization)

    # Set database to tenant_name
    db.choose_tenant(g.organization)
