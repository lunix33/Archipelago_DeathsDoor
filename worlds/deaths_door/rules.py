import json
from typing import Any, ClassVar, Optional, Self, Union

from BaseClasses import CollectionState

from .extract import Rule as ExtractedRule, Term, TermModifierOperator, Null, Group, Conjunction, Disjunction, TermDefinition, RuleJsonSerializer, Boolean
from .abc import ParseObjectHook, Data

class Rule(ParseObjectHook):
    data_dir = Data.data_dir
    data_file = "regions.json"

    _items: ClassVar[set[str]] = set()
    _rules: ClassVar[dict[str, Self]] = {}

    name: str
    logic: ExtractedRule

    def __init__(self, logic: ExtractedRule):
        self.logic = logic

    def evaluate(self, player: int, state: CollectionState, stack: list[str] = []) -> bool:
        return self._evaluate_rule(self.logic, player, state, stack)

    def _evaluate_rule(self, rule: ExtractedRule, player: int, state: CollectionState, stack: list[str]) -> bool:
        if isinstance(rule, Null):
            return True
        if isinstance(rule, Boolean):
            return rule.value
        elif isinstance(rule, Group):
            return self._evaluate_rule(rule.rule, player, state, stack)
        elif isinstance(rule, Term):
            return self._evaluate_term(rule, player, state, stack)
        elif isinstance(rule, Conjunction):
            return self._evaluate_rule(rule.a, player, state, stack) and self._evaluate_rule(rule.b, player, state, stack)
        elif isinstance(rule, Disjunction):
            return self._evaluate_rule(rule.a, player, state, stack) or self._evaluate_rule(rule.b, player, state, stack)
        else:
            raise Exception(f"Invalid rule: {rule}")

    def _evaluate_term(self, term: Term, player: int, state: CollectionState, stack: list[str]) -> bool:
        name = term.to_name()
        term_rule = self._get_by_name(name)

        if isinstance(term_rule, Rule):
            if name in stack:
                raise Exception(f"Circular reference found: {name} (lower: {stack})")
            stack.append(name)
            result = term_rule.evaluate(player, state)
            stack.pop()
            return result

        if isinstance(term_rule, str):
            match term.modifier:
                case (TermModifierOperator.Greater, count_str):
                    count = int(count_str) + 1
                case (TermModifierOperator.Equal, count_str):
                    count = int(count_str)
                case _:
                    count = 1
            return state.has(name, player, count)

        raise Exception(f"Unrecognized term: {term.term}")

    @classmethod
    def add_item(cls, name: str):
        cls._items.add(name)

    @classmethod
    def add_rule(cls, name: str, rule: ExtractedRule):
        cls._rules[name] = cls(rule)

    @classmethod
    def load(cls):
        definitions: list[TermDefinition] = []
        with (cls.data_dir / cls.data_file).open() as file:
            definitions = json.load(file, object_hook=cls.object_hook)
        for definition in definitions:
            cls.add_rule(definition.to_name(), definition.rule)

    @classmethod
    def object_hook(cls, dict: dict[Any, Any]) -> Any:
        return RuleJsonSerializer.object_hook(dict)

    @classmethod
    def _get_by_name(cls, name: str) -> Optional[Union[str, "Rule"]]:
        if name in cls._items:
            return name
        return cls._rules.get(name)
