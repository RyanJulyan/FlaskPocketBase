from flask import current_app as ca


def auth_extension() -> None:
    admin = ca.admin
    # Now you can use the admin instance...
