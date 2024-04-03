import importlib
import sys
from typing import Any, Literal

from app.brokers.storage.list_folders import list_folders
from app.plugins.get_enabled_plugins import get_enabled_plugins

DEFAULT_PLUGINS_DIRECTORY = "app/plugins/"


def register_plugins(
    app: Any,
    plugins_directory: str = DEFAULT_PLUGINS_DIRECTORY,
    get_enabled_plugins_method_name: Literal["json", "sql_alch"] = "json",
) -> None:
    @app.before_request
    def before_request() -> None:
        enabled_plugins = get_enabled_plugins(
            method_name=get_enabled_plugins_method_name
        )  # Get the list of enabled plugins from your database or config file

        all_plugins = list_folders(plugins_directory)

        for plugin in all_plugins:
            if plugin in enabled_plugins and plugin not in sys.modules:
                # The plugin is enabled and not currently registered, so register it
                try:
                    plugin_module = importlib.import_module(
                        f".plugins.{plugin}.view",
                        "app",
                    )
                    getattr(plugin_module, f"{plugin}_plugin")()
                except Exception as e:
                    print(f"Failed to import plugin: `{plugin}`")
                    print(e)
            elif plugin not in enabled_plugins and plugin in sys.modules:
                # The plugin is disabled and currently registered, so unregister it
                try:
                    del sys.modules[plugin]
                except Exception as e:
                    print(f"Failed to unregister plugin: `{plugin}`")
                    print(e)
