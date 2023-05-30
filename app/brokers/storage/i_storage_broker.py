"""
A base class for interfacing with data storage formats (e.g json, sql,
 excel or csv).
"""
from abc import ABC, abstractmethod
from typing import Any


class IStorageBroker(ABC):
    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def read(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, *args: Any, **kwargs: Any) -> Any:
        pass
