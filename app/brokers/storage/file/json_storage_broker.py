import os
import json
from typing import Any, Dict

from app.brokers.storage.i_storage_broker import IStorageBroker


class JsonStorageBroker(IStorageBroker):
    def create(
        self, file_path: str, data: Dict[Any, Any], *args: Any, **kwargs: Any
    ) -> Any:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, *args, **kwargs)

    def read(self, file_path: str, *args: Any, **kwargs: Any) -> Any:
        with open(file_path, "r") as json_file:
            data = json.load(json_file, *args, **kwargs)
        return data

    def update(
        self, file_path: str, data: Dict[Any, Any], *args: Any, **kwargs: Any
    ) -> Any:
        with open(file_path, "r+") as json_file:
            file_data = json.load(json_file)
            file_data.update(data)
            json_file.seek(0)
            json.dump(file_data, json_file, *args, **kwargs)
            json_file.truncate()

    def delete(self, file_path: str) -> Any:
        if os.path.exists(file_path) and file_path.endswith(".json"):
            os.remove(file_path)
