from typing import Any

from flask import g, request

from app.core.choose_tenant.choose_tenant import choose_tenant
from app.core.create_database.create_database import create_database
from app.core.create_tables_from_models.create_tables_from_models import (
    create_tables_from_models,
)
from app.core.create_admin_user.create_admin_user import create_admin_user


appHasRunBefore: bool = False


def before_request(app: Any) -> None:
    @app.before_request
    def before_request() -> None:
        global appHasRunBefore
        choose_tenant(app=app)

        create_database(app=app)

        create_tables_from_models(app=app)

        if not appHasRunBefore:
            create_admin_user(app=app)
            appHasRunBefore = True
