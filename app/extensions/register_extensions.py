import importlib
import sys
from typing import Any, Literal

from app.brokers.storage.list_folders import list_folders
from app.extensions.get_enabled_extensions import get_enabled_extensions

DEFAULT_EXTENSIONS_DIRECTORY = "app/extensions/"


def register_extensions(
    app: Any,
    extensions_directory: str = DEFAULT_EXTENSIONS_DIRECTORY,
    get_enabled_extensions_method_name: Literal["json", "sql_alch"] = "json",
) -> None:
    # @app.before_request
    # def before_request() -> None:
    enabled_extensions = get_enabled_extensions(
        method_name=get_enabled_extensions_method_name
    )  # Get the list of enabled extensions from your database or config file

    all_extensions = list_folders(extensions_directory)

    for extension in all_extensions:
        if extension in enabled_extensions and extension not in sys.modules:
            # The extension is enabled and not currently registered, so register it
            # try:
            extension_module = importlib.import_module(
                f".extensions.{extension}.view",
                "app",
            )
            getattr(extension_module, f"{extension}_extension")(app=app)
        # except Exception as e:
        #     print(f"Failed to import extension: `{extension}`")
        #     print(e)

        elif extension not in enabled_extensions and extension in sys.modules:
            # The extension is disabled and currently registered, so unregister it
            try:
                del sys.modules[extension]
            except Exception as e:
                print(f"Failed to unregister extension: `{extension}`")
                print(e)
