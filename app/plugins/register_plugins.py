import os
import importlib
from typing import Any, List

from app.plugins.get_enabled_plugins import get_enabled_plugins

DEFAULT_PLUGINS_DIRECTORY = "app/plugins/"


def list_folders(directory: str) -> List[str]:
    return [
        d
        for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]


def register_plugins(
    app: Any,
    plugins_directory: str = DEFAULT_PLUGINS_DIRECTORY,
) -> None:
    @app.before_request
    def before_request() -> None:
        enabled_plugins = (
            get_enabled_plugins()
        )  # Get the list of enabled plugins from your database or config file

        all_plugins = list_folders(plugins_directory)

        for plugin in all_plugins:
            if plugin in enabled_plugins and plugin not in app.blueprints:
                # The plugin is enabled and not currently registered, so register it
                try:
                    blueprint = importlib.import_module(
                        f".plugins.{plugin}.view", "app"
                    ).blueprint
                    app.register_blueprint(blueprint)
                except Exception as e:
                    print(f"Failed to import plugin: `{plugin}`")
                    print(e)
            elif plugin not in enabled_plugins and plugin in app.blueprints:
                # The plugin is disabled and currently registered, so unregister it
                try:
                    app.blueprints.pop(plugin)
                except Exception as e:
                    print(f"Failed to unregister plugin: `{plugin}`")
                    print(e)
