from flask import current_app


def storage_extension() -> None:
    admin = current_app.admin
    # Now you can use the admin instance...
