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

    def get_engine(self, bind_key: str = None):
        if bind_key is None:
            if not hasattr(g, "tenant"):
                raise RuntimeError("No tenant chosen.")
            bind_key = g.tenant
        return super().get_engine(bind_key=bind_key)
