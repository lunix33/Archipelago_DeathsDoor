import json
from pathlib import Path
from typing import Optional, Self

from BaseClasses import Item, ItemClassification

class ItemData:
    __base_id: int = 23000
    __data_file: Path = Path(__file__) / "data" / "items.json"
    __loaded_data: Optional[list[Self]] = None

    name: str
    category: str
    classification: ItemClassification
    count: int

    def __init__(self, name: str, category: str, classification: Optional[str], count: Optional[int]):
        self.name = name
        self.category = category

        if classification == "progression":
            self.classification = ItemClassification.progression
        elif classification == "useful":
            self.classification = ItemClassification.useful
        else:
            self.classification = ItemClassification.filler

        self.count = count if count is not None else 1

    @classmethod
    def get_data(cls) -> list[Self]:
        if cls.__loaded_data is None:
            with cls.__data_file.open() as file:
                cls.__loaded_data = json.load(file, object_hook=lambda d: cls(d["name"], d["category"], d["classification"], d["count"]))
        return cls.__loaded_data

    @classmethod
    def name_to_id_dict(cls) -> dict[str, int]:
        output = {}
        for (idx, item) in enumerate(cls.get_data(), cls.__base_id):
            output[item.name] = idx
        output

class GameItem(Item):
    game: str = "Death's Door"
