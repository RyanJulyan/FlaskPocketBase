from typing import Any

from flask_security import Security, SQLAlchemyUserDatastore

from app.models.data.role import Role
from app.models.data.user import User


def init_flask_admin(
    app: Any,
    name: str = "FLaskPocketBase",
    template_mode: str = "bootstrap4",
    **kwargs: Any
) -> Security:
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(app.db, User, Role)
    security = Security(app, user_datastore)

    return security
