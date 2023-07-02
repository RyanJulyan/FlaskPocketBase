from typing import Any
import json

from werkzeug.exceptions import HTTPException
from flask import make_response


def errorhandler(app: Any) -> None:
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = make_response()

        code = 500
        name = "Server Error"
        description = "Internal Server Error"

        if isinstance(e, HTTPException):
            response = e.get_response()

            code = e.code
            name = e.name
            description = e.description

        else:
            name = str(type(e).__name__)
            description = str(e)

        # start with the correct headers and status code from the error
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": code,
                "name": name,
                "description": description,
            }
        )

        response.status = code
        response.content_type = "application/json"
        return response
