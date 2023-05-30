"""
A base class for interfacing with data storage formats (e.g json, sql,
 excel or csv).
"""
from abc import ABC, abstractmethod
from typing import Any


class IService(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def read_single(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def read_all(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> Any:
        pass
