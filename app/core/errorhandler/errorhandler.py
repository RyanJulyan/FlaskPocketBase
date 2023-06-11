from typing import Any
import json

from werkzeug.exceptions import HTTPException
from flask import make_response


def errorhandler(app: Any) -> None:
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        code = 500
        name = "Server Error"
        description = "Internal Server Error"
        response = make_response()
        if isinstance(e, HTTPException):
            code = e.code
            name = e.name
            description = e.description

            response = e.get_response()
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
        response.content_type = "application/json"
        return response
