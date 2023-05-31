from typing import Callable, Dict, Any, List
import json

from app.brokers.storage.i_storage_broker import IStorageBroker
from app.brokers.storage.file.json_storage_broker import JsonStorageBroker

# from app.plugins.sql_alch_model_plugin import Plugin


def get_enabled_plugins_json(
    file_path: str = "configuration/enabled_plugins.json",
    StorageBroker: IStorageBroker = JsonStorageBroker(),
) -> List[str]:
    enabled_plugins = StorageBroker.read(file_path=file_path)
    return enabled_plugins


# def get_enabled_plugins_sql_alch() -> List[str]:
#     enabled_plugins = Plugin.query.filter_by(enabled=True).all()
#     return [plugin.name for plugin in enabled_plugins]


def get_enabled_plugins(method_name: str = "json", **kwargs: Any) -> List[str]:
    methods: Dict[str, Callable[..., Any]] = {
        # "sql_alch": get_enabled_plugins_sql_alch,
        "json": get_enabled_plugins_json,
    }

    return methods[method_name](**kwargs)
