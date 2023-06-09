from typing import Any

from flask import g, request
from sqlalchemy_utils import database_exists, create_database

from app.core.database.database import db


def before_request(app: Any) -> None:
    @app.before_request
    def before_request() -> None:
        # organization = tenant_name
        # Just use the query parameter "?organization=tenant_name"
        # or a subdomain tenant_name.example.com
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

        # Create database if it does not exist.
        if app.config["AUTO_CREATE_DATABASE"]:
            if not database_exists(db.get_engine().url):
                create_database(db.get_engine().url)
            else:
                # Connect the database if exists.
                db.get_engine().connect()

        # Build the database:
        if app.config["AUTO_CREATE_TABLES_FROM_MODELS"]:
            # This will create the database tables using SQLAlchemy
            with app.app_context():
                db.create_all()
