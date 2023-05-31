from typing import Any
from flask import g
from flask_sqlalchemy import SQLAlchemy


class MultiTenantSQLAlchemy(SQLAlchemy):
    def choose_tenant(self, bind_key: str):
        if hasattr(g, "tenant"):
            raise RuntimeError(
                "Switching tenant in the middle of the request."
            )
        g.tenant = bind_key

    def get_engine(self, app: Any = None, bind: str = None):
        if bind is None:
            if not hasattr(g, "tenant"):
                raise RuntimeError("No tenant chosen.")
            bind = g.tenant
        return super().get_engine(app=app, bind=bind)
