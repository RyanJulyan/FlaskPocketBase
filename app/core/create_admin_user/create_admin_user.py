from typing import Any

from app.core.database.database import db


def create_admin_user(app: Any):

    # Add Admin user:
    if app.config["AUTO_CREATE_ADMIN_USER"]:
        # This will create the admin user using `flask_security` and SQLAlchemyUserDatastore
        with app.app_context():
            app.user_datastore.create_user(
                email=app.config["ADMIN_EMAIL"],
                password=app.config["ADMIN_PASSWORD"],
            )
            db.session.commit()
