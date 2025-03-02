from typing import Any, Optional

from BaseClasses import Item, ItemClassification

from .abc import Data, Idable

class ItemData(Data, Idable):
    data_file = "items.json"

    name: str
    category: str
    classification: ItemClassification
    count: int

    def __init__(self, name: str, category: str, classification: Optional[str], count: Optional[int]):
        self.name = name
        self.category = category

        self.count = count if count is not None else 1

        if classification == "progression":
            self.classification = ItemClassification.progression
        elif classification == "useful":
            self.classification = ItemClassification.useful
        else:
            self.classification = ItemClassification.filler

    def to_game_item(self, player: int) -> "GameItem":
        return GameItem(self, player)

    @classmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        name = dict.get("name")
        if name is None:
            raise Exception(f"Invalid structure. No name found: {dict}")
        category = dict.get("category")
        if category is None:
            raise Exception(f"Invalid structure. No category found: {dict}")
        classification = dict.get("classification")
        count = dict.get("count")
        return cls(name, category, classification, count)

class GameItem(Item):
    game: str = "Death's Door"
    data: ItemData

    def __init__(self, data: ItemData, player: int):
        self.data = data
        super().__init__(data.name, data.classification, data.id(), player)
