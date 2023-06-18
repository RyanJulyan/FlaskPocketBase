from typing import Any

from flask import g, request
from flask_restx import Resource


def health_check_api(app: Any, api: Any, **kwargs: Any) -> None:
    # Swagger namespace
    ns = api.namespace(
        "api/health_check",
        description="A health check API",
    )

    @ns.route("/")
    class HealthCheckListResource(Resource):
        @ns.doc(
            responses={
                200: "OK",
                422: "Unprocessable Entity",
                500: "Internal Server Error",
            },
            description="get insights",
        )
        def get(self):  # /health_check
            """List Health Check records"""
            return {
                "status": 200,
                "message": "healthy",
                "organization": g.organization,
                "site_title": app.config["SITE_TITLE"],
                "expected_site_url": app.config["SITE_URL"],
                "actual_site_url": request.environ.get("HTTP_HOST"),
                **kwargs,
            }, 200
