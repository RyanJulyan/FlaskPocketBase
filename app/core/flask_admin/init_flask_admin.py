from typing import Any

from flask_admin import Admin


def init_flask_admin(
    app: Any,
    name: str = "FLaskPocketBase",
    **kwargs: Any,
) -> Admin:
    # Initialize Flask-Admin
    app.admin = Admin(
        app,
        name=name,
        **kwargs,
    )

    return app
