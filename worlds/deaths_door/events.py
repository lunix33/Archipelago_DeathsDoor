from typing import Any, Optional

from BaseClasses import Item, Location, ItemClassification, Region

from .extract import RuleJsonSerializer, TermDefinition
from .abc import Data
from .rules import Rule

class EventData(Data):
    data_file = "events.json"

    name: str
    rule: Rule

    def __init__(self, name: str, rule: Rule):
        self.name = name
        self.rule = rule

        Rule.add_item(self.name)

    def to_game_event(self, player: int, parent: Region) -> "EventLocation":
        return EventLocation(self, player, parent)

    @classmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        definition = RuleJsonSerializer.object_hook(dict)
        if not isinstance(definition, TermDefinition):
            return definition
        return cls(definition.to_name(), Rule(definition.rule))

class EventItem(Item):
    game = "Death's Door"

    def __init__(self, location: "EventLocation"):
        super().__init__(location.name, ItemClassification.progression, None, location.player)

class EventLocation(Location):
    game = "Death's Door"

    data: EventData

    def __init__(self, data: EventData, player: int, parent: Optional[Region] = None):
        super().__init__(player, data.name, None, parent)
        self.place_locked_item(EventItem(self))
        self.access_rule = lambda _: True
