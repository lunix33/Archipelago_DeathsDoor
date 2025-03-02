from typing import ClassVar, Optional, Self, Union

from BaseClasses import CollectionState

from .extract import Rule as ExtractedRule, Term, TermModifierOperator, Null, Group, Conjunction, Disjunction

class RuleRegistry:
    _items: set[str]
    _rules: dict[str, "Rule"]

    def __init__(self):
        self._items = set()
        self._rules = {}

    def add_item(self, name: str):
        self._items.add(name)

    def add_rule(self, name: str, rule: ExtractedRule):
        self._rules[name] = Rule(rule)

    def get(self, name: str) -> Optional[Union[str, "Rule"]]:
        if name in self._items:
            return name
        return self._rules.get(name)

class Rule:
    _items: ClassVar[set[str]] = set()
    _rules: ClassVar[dict[str, Self]] = {}

    logic: ExtractedRule

    def __init__(self, logic: ExtractedRule):
        self.logic = logic

    def evaluate(self, player: int, state: CollectionState, registry: RuleRegistry) -> bool:
        return self._evaluate_rule(self.logic, player, state, registry)

    def _evaluate_rule(self, rule: ExtractedRule, player: int, state: CollectionState, registry: RuleRegistry) -> bool:
        if isinstance(rule, Null):
            return True
        elif isinstance(rule, Group):
            return self._evaluate_rule(rule.rule, player, state, registry)
        elif isinstance(rule, Term):
            return self._evaluate_term(rule, player, state, registry)
        elif isinstance(rule, Conjunction):
            return self._evaluate_rule(rule.a, player, state, registry) and self._evaluate_rule(rule.b, player, state, registry)
        elif isinstance(rule, Disjunction):
            return self._evaluate_rule(rule.a, player, state, registry) or self._evaluate_rule(rule.b, player, state, registry)
        else:
            return False

    def _evaluate_term(self, term: Term, player: int, state: CollectionState, registry: RuleRegistry) -> bool:
        name = term.to_name()
        term_rule = self._get_by_name(name)

        if isinstance(term_rule, Rule):
            return term_rule.evaluate(player, state, registry)

        if isinstance(term_rule, str):
            match term.modifier:
                case (TermModifierOperator.Greater, count_str):
                    count = int(count_str) + 1
                case (TermModifierOperator.Equal, count_str):
                    count = int(count_str)
                case _:
                    count = 1
            return state.has(name, player, count)

        print(f"Unrecognized term: {term.term}")
        return False

    @classmethod
    def add_item(cls, name: str):
        cls._items.add(name)

    @classmethod
    def add_rule(cls, name: str, rule: ExtractedRule):
        cls._rules[name] = cls(rule)

    @classmethod
    def _get_by_name(cls, name: str) -> Optional[Union[str, "Rule"]]:
        if name in cls._items:
            return name
        return cls._rules.get(name)
