import os
from typing import Any

from flask import g, request
from flask_restx import Resource
from jinja2 import ChoiceLoader, FileSystemLoader


def health_check_api(app: Any, **kwargs: Any) -> None:
    # Namespace-specific template folder
    current_dir = os.path.dirname(__file__)
    namespace_template_folder = os.path.join(current_dir, "templates")

    # Extend the Jinja2 loader to include the namespace templates
    app.jinja_loader = ChoiceLoader(
        [
            app.jinja_loader,  # Default loader
            FileSystemLoader(
                namespace_template_folder
            ),  # Namespace-specific folder
        ]
    )

    # Swagger namespace
    ns = app.api.namespace(
        "api/health_check",
        description="A health check API",
    )

    @ns.route("")
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
            data = {
                "status": 200,
                "message": "healthy",
                "organization": g.organization,
                "site_title": app.config["SITE_TITLE"],
                "expected_site_url": app.config["SITE_URL"],
                "actual_site_url": request.environ.get("HTTP_HOST"),
                **kwargs,
            }

            return data, 200
            # return data, 200, {"X-TEMPLATE": "healthcheck.html"}
            # return app.api.render_response(data, template="healthcheck.html")
