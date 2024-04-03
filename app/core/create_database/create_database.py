from typing import Any

from sqlalchemy_utils import database_exists, create_database

from app.core.database.database import db


def create_database(app: Any):
    # Create database if it does not exist.
    if app.config["AUTO_CREATE_DATABASE"]:
        if not database_exists(db.get_engine().url):
            create_database(db.get_engine().url)
        else:
            # Connect the database if exists.
            db.get_engine().connect()
