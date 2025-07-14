from typing import Any
from flask_talisman.talisman import Talisman


def init_flask_talisman(app: Any):
    app.talisman = Talisman(
        app=app,
        content_security_policy=app.config["CONTENT_SECURITY_POLICY"],
        content_security_policy_report_uri=app.config[
            "CONTENT_SECURITY_POLICY_REPORT_URI"
        ],
        content_security_policy_report_only=False,
        session_cookie_secure=app.config["SESSION_COOKIE_SECURE"],
        session_cookie_http_only=app.config["SESSION_COOKIE_HTTPONLY"],
        session_cookie_samesite=app.config["SESSION_COOKIE_SAMESITE"],
        x_xss_protection=app.config["X_XSS_PROTECTION"],
        x_content_type_options=app.config["X_CONTENT_TYPE_OPTIONS"],
        frame_options=app.config["FRAME_OPTIONS"],
        force_https=app.config["FORCE_HTTPS"],
        strict_transport_security=app.config["STRICT_TRANSPORT_SECURITY"],
        strict_transport_security_max_age=app.config[
            "STRICT_TRANSPORT_SECURITY_MAX_AGE"
        ],
        strict_transport_security_include_subdomains=app.config[
            "STRICT_TRANSPORT_SECURITY_INCLUDE_SUBDOMAINS"
        ],
    )

    return app
