from typing import Any

from flask import g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker


class MultiTenantSQLAlchemy(SQLAlchemy):
    """Custom SQLAlchemy class for handling multi-tenancy."""

    def get_bind(self, mapper=None, clause=None):
        """Dynamically choose the correct tenant database."""
        tenant = getattr(g, "tenant", "default")
        return self.engines.get(tenant, self.engines["default"])

    def choose_tenant(self, bind_key):
        """Set the tenant database bind key for the current request."""
        g.tenant = bind_key

    def get_session(self):
        """Return a session bound to the correct tenant database."""
        engine = self.get_bind()
        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)
