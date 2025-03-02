from typing import Any, Self

from BaseClasses import Location, Region

from .abc import Data, Idable
from .extract import RuleJsonSerializer, TermDefinition

class LocationData(Data, Idable):
    data_file = "locations.json"

    name: str
    term: str

    def __init__(self, term: str):
        self.name = term.replace("_", " ")
        self.term = term

    def to_game_location(self, player: int, region: Region) -> "GameLocation":
        return GameLocation(self, player, region)

    @classmethod
    def from_dict(cls, dict: dict[Any, Any]) -> Self:
        definition = RuleJsonSerializer.from_dict(dict)
        if not isinstance(definition, TermDefinition):
            return definition
        return cls(definition.term)

class GameLocation(Location):
    game: str = "Death's Door"
    data: LocationData

    def __init__(self, data: LocationData, player: int, parent = None):
        self.data = data
        super().__init__(player, data.name, data.id(), parent)
