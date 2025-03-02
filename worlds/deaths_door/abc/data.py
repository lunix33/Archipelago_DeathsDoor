from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any, Optional, Self

class Data(ABC):
    __loaded_data: Optional[list[Self]] = None
    __data_dir: Path = Path(__file__).parent.parent / "data"
    data_file: str

    @classmethod
    @abstractmethod
    def from_dict(cls, dict: dict[Any, Any]) -> Self:
        pass

    @classmethod
    def get_data(cls) -> list[Self]:
        if cls.__loaded_data is None:
            cls.load()
        return cls.__loaded_data

    @classmethod
    def load(cls):
        if cls.__loaded_data is not None:
            return

        with (cls.__data_dir / cls.data_file).open() as file:
            cls.__loaded_data = json.load(file, object_hook=cls.from_dict)
