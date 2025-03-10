from abc import ABC
import json
from pathlib import Path
from typing import ClassVar, Optional, Self

from .parse_object_hook import ParseObjectHook

class Data(ParseObjectHook, ABC):
    _loaded_data: ClassVar[Optional[list[Self]]] = None
    data_dir: ClassVar[Path] = Path(__file__).parent.parent / "data"
    data_file: ClassVar[str]

    @classmethod
    def get_data(cls) -> list[Self]:
        if cls._loaded_data is None:
            cls.load()
        return cls._loaded_data or []

    @classmethod
    def load(cls):
        if cls._loaded_data is not None:
            return

        with (cls.data_dir / cls.data_file).open() as file:
            cls._loaded_data = json.load(file, object_hook=cls.object_hook)
