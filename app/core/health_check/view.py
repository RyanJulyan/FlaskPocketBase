from typing import Any

from flask import g, jsonify, request


def health_check(app: Any, **kwargs: Any) -> None:
    @app.route("/health_check")
    def health_check() -> None:
        return jsonify(
            {
                "status": 200,
                "message": "healthy",
                "organization": g.organization,
                "site_title": app.config["SITE_TITLE"],
                "expected_site_url": app.config["SITE_URL"],
                "actual_site_url": request.environ.get("HTTP_HOST"),
                **kwargs,
            }
        )
