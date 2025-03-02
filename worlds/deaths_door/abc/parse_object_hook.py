from abc import ABC, abstractmethod
from typing import Any

class ParseObjectHook(ABC):
    @classmethod
    @abstractmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        pass
