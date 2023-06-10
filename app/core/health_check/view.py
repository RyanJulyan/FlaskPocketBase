from typing import Any

from flask import g, jsonify


def health_check(app: Any) -> None:
    @app.route("/health_check")
    def health_check() -> None:
        return jsonify(
            {
                "status": 200,
                "message": "healthy",
                "organization": g.organization,
                "site_title": app.config["SITE_TITLE"],
                "site_url": app.config["SITE_URL"],
            }
        )
