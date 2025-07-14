from typing import Any

from flask import g

from app.services.util.make_serializable import make_serializable


def context_processor(app: Any) -> None:
    @app.context_processor
    def context_processor() -> None:
        return {
            "organization": getattr(g, "organization", "No Organization Set"),
            "make_serializable": make_serializable,
        }
