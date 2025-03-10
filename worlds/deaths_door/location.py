from typing import Any, Optional

from BaseClasses import Location, Region

from .abc import Data, Idable
from .extract import RuleJsonSerializer, TermDefinition
from .rules import Rule

class LocationData(Data, Idable):
    data_file = "locations.json"

    name: str
    rule: Rule

    def __init__(self, name: str, rule: Rule):
        self.name = name
        self.rule = rule

    def to_game_location(self, player: int, region: Region) -> "GameLocation":
        return GameLocation(self, player, region)

    @classmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        definition = RuleJsonSerializer.object_hook(dict)
        if not isinstance(definition, TermDefinition):
            return definition
        return cls(definition.to_name(), Rule(definition.rule))

class GameLocation(Location):
    game: str = "Death's Door"
    data: LocationData

    def __init__(self, data: LocationData, player: int, parent: Optional[Region] = None):
        self.data = data
        self.access_rule = lambda state: self.data.rule.evaluate(player, state)
        super().__init__(player, data.name, data.id(), parent)
