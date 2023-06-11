from flask import current_app as ca


def storage_extension() -> None:
    admin = ca.admin
    # Now you can use the admin instance...
