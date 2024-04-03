from typing import Any
from flask import current_app as ca


def storage_extension(app: Any) -> None:
    app.admin
    # Now you can use the admin instance...
