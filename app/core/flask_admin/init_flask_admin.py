from typing import Any

from flask_admin import Admin


def init_flask_admin(
    app: Any,
    name: str = "FLaskPocketBase",
    template_mode: str = "bootstrap4",
    **kwargs: Any
) -> Admin:
    # Initialize Flask-Admin
    admin = Admin(
        app,
        name=name,
        template_mode=template_mode,
        **kwargs,
    )

    return admin
