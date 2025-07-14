import csv
import io

from dicttoxml import dicttoxml  # For XML formatting
from flask_restx import Api
from flask import (
    request,
    make_response,
    jsonify,
    render_template,
    current_app as ca,
)
from pandas import DataFrame

from app.services.util.make_serializable import make_serializable


class CustomApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.representations = {}  # Remove default JSON renderer

    def make_response(self, data, *args, code=200, headers=None, **kwargs):
        """
        Override default response generation with format-aware rendering.
        """
        template_name = None
        if headers and "X-TEMPLATE" in headers:
            template_name = headers.pop("X-TEMPLATE")

        if request.args and (
            "TEMPLATE" in request.args or "template" in request.args
        ):
            template_name = request.args.get("template") or request.args.get(
                "TEMPLATE"
            )

        response = self.render_response(data, template_name=template_name)
        response.status_code = code
        if headers:
            response.headers.extend(headers)
        return response

    def render_response(self, data, *args, template_name=None, **kwargs):
        format_type = request.args.get("format", "json").lower()
        serializable_data = make_serializable(data)
        filename = request.path.strip("/").replace("/", "_") or "data"

        if format_type == "xml":
            response = make_response(
                dicttoxml(serializable_data, custom_root="response")
            )
            if request.args.get("download", "false").lower() == "true":
                response.headers["Content-Disposition"] = (
                    f"attachment; filename={filename}.xml"
                )
            response.headers["Content-Type"] = "application/xml"

        elif format_type == "html":
            if template_name:
                response = make_response(
                    render_template(template_name, data=serializable_data)
                )
            else:
                # Attempt to convert to a DataFrame if possible
                html_table = ""
                try:
                    if isinstance(serializable_data, list) and all(
                        isinstance(row, dict) for row in serializable_data
                    ):
                        df = DataFrame(serializable_data)
                    elif isinstance(serializable_data, dict):
                        df = DataFrame([serializable_data])
                    else:
                        raise ValueError(
                            "Unsupported format for table rendering"
                        )

                    html_table = df.to_html(
                        index=False,
                        classes="table table-bordered table-striped",
                        border=0,
                    )
                except Exception as e:
                    html_table = f"<pre>{str(serializable_data)}</pre>"

                response = make_response(
                    f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{filename}</title>
                        <style>
                            body {{ font-family: sans-serif; padding: 2em; }}
                            .table {{ border-collapse: collapse; width: 100%; }}
                            .table td, .table th {{ border: 1px solid #ddd; padding: 8px; }}
                            .table th {{ background-color: #f2f2f2; }}
                        </style>
                    </head>
                    <body>
                        {html_table}
                    </body>
                    </html>
                    """
                )

            if request.args.get("download", "false").lower() == "true":
                response.headers["Content-Disposition"] = (
                    f"attachment; filename={filename}.html"
                )
            response.headers["Content-Type"] = "text/html"

        elif format_type == "csv":
            output = io.StringIO()
            writer = csv.writer(
                output,
                delimiter=(
                    request.args.get("delimiter")
                    or ca.config.get("CSV_DELIMITER", "|")
                ),
            )

            # Handle list of dicts
            if isinstance(serializable_data, list) and all(
                isinstance(row, dict) for row in serializable_data
            ):
                headers = serializable_data[0].keys()
                writer.writerow(headers)
                for row in serializable_data:
                    writer.writerow([row.get(h, "") for h in headers])

            # Handle single dict
            elif isinstance(serializable_data, dict):
                writer.writerow(serializable_data.keys())
                writer.writerow(serializable_data.values())

            # Handle flat list
            elif isinstance(serializable_data, list):
                for item in serializable_data:
                    writer.writerow([item])

            else:
                writer.writerow([str(serializable_data)])

            csv_data = output.getvalue()
            output.close()

            response = make_response(csv_data)
            if request.args.get("download", "false").lower() == "true":
                response.headers["Content-Disposition"] = (
                    f"attachment; filename={filename}.csv"
                )
                response.headers["Content-Type"] = "text/csv"
            else:
                response.headers["Content-Disposition"] = "inline"
                response.headers["Content-Type"] = "text/text"

        else:  # Default: JSON
            response = make_response(jsonify(serializable_data))
            if request.args.get("download", "false").lower() == "true":
                response.headers["Content-Disposition"] = (
                    f"attachment; filename={filename}.json"
                )
            response.headers["Content-Type"] = "application/json"

        return response
