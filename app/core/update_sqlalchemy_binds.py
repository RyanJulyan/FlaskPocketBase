from app import app, db


def update_sqlalchemy_binds(new_bind_key: str, new_bind_uri: str) -> None:
    app.config["SQLALCHEMY_BINDS"][new_bind_key] = new_bind_uri
    db.get_engine(
        app, bind=new_bind_key
    )  # This will create a new engine for the new bind
