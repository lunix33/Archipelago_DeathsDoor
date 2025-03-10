from typing import Any, Optional

from BaseClasses import Item, ItemClassification, Location, Region

from .abc import Data, ParseObjectHook
from .rules import Rule
from .extract import TermDefinition, RuleJsonSerializer

class EntranceData(Data, ParseObjectHook):
    data_file = "entrances.json"

    name: str
    rule: Rule

    def __init__(self, name: str, rule: Rule) -> None:
        self.name = name
        self.rule = rule

        Rule.add_item(self.name)

    def to_game_transition(self, player: int, parent: Region) -> "EntranceLocation":
        return EntranceLocation(self, player, parent)

    @classmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        definition = RuleJsonSerializer.object_hook(dict)
        if not isinstance(definition, TermDefinition):
            return definition
        return cls(definition.to_name(), Rule(definition.rule))

class EntranceItem(Item):
    game = "Death's Door"
    
    def __init__(self, location: "EntranceLocation"):
        super().__init__(location.name, ItemClassification.progression, None, location.player)

class EntranceLocation(Location):
    game = "Death's Door"

    data: EntranceData

    def __init__(self, data: EntranceData, player: int, parent: Optional[Region] = None):
        self.data = data
        super().__init__(player, data.name, None, parent)
        self.place_locked_item(EntranceItem(self))
        self.access_rule = lambda state: self.data.rule.evaluate(player, state)
