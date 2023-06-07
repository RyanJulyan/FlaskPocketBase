from typing import Any

from flask import g


def context_processor(app: Any):
    @app.context_processor
    def get_additional_data_context_in_template():
        return {
            "organization": g.organization,
        }
