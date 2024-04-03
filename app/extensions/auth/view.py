from typing import Any

from flask import current_app as ca
from flask_admin.contrib.sqla import ModelView

from app.core.database.database import db
from app.models.data.role import Role
from app.models.data.user import User


def auth_extension(app: Any) -> None:
    print(__name__)

    app.admin.add_view(ModelView(User, db.session))
    app.admin.add_view(ModelView(Role, db.session))
