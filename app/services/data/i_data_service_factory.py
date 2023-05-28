from abc import ABC
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class IDataServiceFactory(ABC):
    functions: ClassVar = None
