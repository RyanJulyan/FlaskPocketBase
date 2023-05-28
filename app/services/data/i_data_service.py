"""
A base class for interfacing with data storage formats (e.g json, sql,
 excel or csv).
"""
from abc import ABC, abstractmethod


class IService(ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_single(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
