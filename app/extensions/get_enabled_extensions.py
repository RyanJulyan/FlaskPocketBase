from typing import Callable, Dict, Any, List
import json

from app.brokers.storage.i_storage_broker import IStorageBroker
from app.brokers.storage.file.json_storage_broker import JsonStorageBroker
from app.models.data.extension import Extension


def get_enabled_extensions_json(
    file_path: str = "configuration/enabled_extensions.json",
    StorageBroker: IStorageBroker = JsonStorageBroker(),
) -> List[str]:
    enabled_extensions = StorageBroker.read(file_path=file_path)
    return enabled_extensions


def get_enabled_extensions_sql_alch() -> List[str]:
    enabled_extensions = Extension.query.filter_by(enabled=True).all()
    return [extension.name for extension in enabled_extensions]


def get_enabled_extensions(
    method_name: str = "json", **kwargs: Any
) -> List[str]:
    methods: Dict[str, Callable[..., Any]] = {
        "sql_alch": get_enabled_extensions_sql_alch,
        "json": get_enabled_extensions_json,
    }

    return methods[method_name](**kwargs)
