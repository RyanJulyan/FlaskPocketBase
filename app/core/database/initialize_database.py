from flask import current_app as ca
from app.core.database.database import db


def initialize_database(tenant):
    """Ensure tables exist in the tenant's database before using it."""
    with ca.app_context():
        chosen_engine = db.engines.get(tenant, db.engines["default"])
        Base.metadata.create_all(bind=chosen_engine)
