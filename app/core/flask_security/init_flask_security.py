from typing import Any

from flask_security import Security, SQLAlchemyUserDatastore

from app.core.database.database import db
from app.models.data.role import Role
from app.models.data.user import User


def init_flask_security(
    app: Any,
    **kwargs: Any,
) -> Security:
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    return security
