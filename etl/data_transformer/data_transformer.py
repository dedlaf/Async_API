from abc import ABC, abstractmethod
from typing import Any


class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data: list[Any]) -> list[Any]: ...
