from app.core.database.database import db
from flask import current_app as ca


def update_sqlalchemy_binds(new_bind_key: str, new_bind_uri: str) -> None:
    ca.config["SQLALCHEMY_BINDS"][new_bind_key] = new_bind_uri
    db.get_engine(
        ca, bind=new_bind_key
    )  # This will create a new engine for the new bind
