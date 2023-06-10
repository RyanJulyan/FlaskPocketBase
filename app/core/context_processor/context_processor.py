from typing import Any

from flask import g


def context_processor(app: Any) -> None:
    @app.context_processor
    def context_processor() -> None:
        return {
            "organization": g.organization,
        }
