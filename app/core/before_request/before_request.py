from typing import Any

from flask import g, request


def before_request(app: Any):
    @app.before_request
    def before_request():
        # organization = tenant_name
        # Just use the query parameter "?organization=tenant_name"
        # or a subdomain tenant_name.example.com
        g.organization = "default"

        host = request.environ.get("HTTP_HOST").split(".")

        if "organization" in request.args:
            g.organization = request.args["organization"]
            app.logger.info("Organisation changed: " + g.organization)
        elif len(host) == 3 and host[0] != "www":
            g.organization = host[0]
            app.logger.info("Organisation changed: " + g.organization)
