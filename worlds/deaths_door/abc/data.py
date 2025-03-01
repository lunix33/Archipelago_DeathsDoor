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
    def load_get(cls) -> list[Self]:
        if cls.__loaded_data is None:
            with (cls.__data_dir / cls.data_file).open() as file:
                cls.__loaded_data = json.load(file, object_hook=cls.from_dict)
        return cls.__loaded_data
