"""
A base class for interfacing with data storage formats (e.g json, sql,
 excel or csv).
"""
from abc import ABC, abstractmethod

class IStorageBroker(ABC):

  @abstractmethod
  def create():
    pass

  @abstractmethod
  def read():
    pass

  @abstractmethod
  def update():
    pass

  @abstractmethod
  def delete():
    pass
