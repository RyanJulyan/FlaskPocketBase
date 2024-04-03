from typing import Any

from app.core.database.database import db


def create_tables_from_models(app: Any):
    # Build the database:
    if app.config["AUTO_CREATE_TABLES_FROM_MODELS"]:
        # This will create the database tables using SQLAlchemy
        with app.app_context():
            db.create_all()
