import os
import importlib
from typing import Any, List, Literal

from app.extensions.get_enabled_extensions import get_enabled_extensions

DEFAULT_EXTENSIONS_DIRECTORY = "app/extensions/"


def list_folders(directory: str) -> List[str]:
  return [
    d for d in os.listdir(directory)
    if os.path.isdir(os.path.join(directory, d))
  ]


def register_extensions(
  app: Any,
  extensions_directory: str = DEFAULT_EXTENSIONS_DIRECTORY,
  get_enabled_extensions_method_name: Literal["json", "sql_alch"] = "json",
) -> None:

  @app.before_request
  def before_request() -> None:
    enabled_extensions = get_enabled_extensions(
      method_name=get_enabled_extensions_method_name
    )  # Get the list of enabled extensions from your database or config file

    all_extensions = list_folders(extensions_directory)

    for extension in all_extensions:
      if (extension in enabled_extensions and extension not in app.blueprints):
        # The extension is enabled and not currently registered, so register it
        try:
          blueprint = importlib.import_module(f".extensions.{extension}.view",
                                              "app").blueprint
          app.register_blueprint(blueprint)
        except Exception as e:
          print(f"Failed to import extension: `{extension}`")
          print(e)

      elif (extension not in enabled_extensions
            and extension in app.blueprints):
        # The extension is disabled and currently registered, so unregister it
        try:
          app.blueprints.pop(extension)
        except Exception as e:
          print(f"Failed to unregister extension: `{extension}`")
          print(e)
