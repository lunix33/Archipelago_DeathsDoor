from abc import ABC, abstractmethod
from typing import ClassVar, Optional, Self

class Idable(ABC):
    _base_id: ClassVar[int] = 23000
    _name_to_id_dict: ClassVar[Optional[dict[str, int]]] = None

    name: str

    def id(self) -> int:
        return self.name_to_id_dict()[self.name]

    @classmethod
    @abstractmethod
    def get_data(cls) -> list[Self]:
        pass

    @classmethod
    def from_name(cls, name: str) -> Optional[Self]:
        id = cls.name_to_id_dict().get(name)
        if id is None:
            return None

        idx = id - cls._base_id
        data = cls.get_data()
        if idx < 0 or idx >= len(data):
            return None

        return data[idx]

    @classmethod
    def name_to_id_dict(cls) -> dict[str, int]:
        if cls._name_to_id_dict is None:
            cls._name_to_id_dict = {}
            for idx, item in enumerate(cls.get_data()):
                cls._name_to_id_dict[item.name] = cls._base_id + idx
        return cls._name_to_id_dict
