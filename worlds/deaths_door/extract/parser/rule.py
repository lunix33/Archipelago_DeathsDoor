
from abc import ABC, abstractmethod
from enum import StrEnum, auto
from json import JSONEncoder
from typing import Any, Optional, Self

class RuleJsonSerializer(JSONEncoder):
    def default(self, o):
        obj_dict = o.__dict__
        if isinstance(o, Null):
            obj_dict["type"] = "null"
        if isinstance(o, Conjunction):
            obj_dict["type"] = "conjunction"
        if isinstance(o, Disjunction):
            obj_dict["type"] = "disjunction"
        if isinstance(o, Group):
            obj_dict["type"] = "group"
        if isinstance(o, Term):
            obj_dict["type"] = "term"
        return obj_dict

    @staticmethod
    def from_dict(dict: dict[Any, Any]):
        match dict.get("type"):
            case "null":
                return Null()
            case "conjunction":
                return Conjunction(dict.get("a"), dict.get("b"))
            case "disjunction":
                return Disjunction(dict.get("a"), dict.get("b"))
            case "group":
                return Group(dict.get("rule"))
            case "term":
                return Term(dict.get("term"), dict.get("modifier"))
            case _:
                return TermDefinition(dict.get("stateless"), dict.get("term"), dict.get("rule"))

class TermDefinition:
    stateless: bool
    term: str
    rule: "Rule"

    def __init__(self, stateless: bool, term: str, rule: Optional["Rule"] = None) -> None:
        self.stateless = stateless
        self.term = term
        self.rule = rule or Null()
    
    def __str__(self) -> str:
        return f"{"stateless " if self.stateless else ""}{self.term}: {self.rule}"

class TermModifierOperator(StrEnum):
    Equal = auto()
    Greater = auto()

    def __str__(self):
        match self:
            case TermModifierOperator.Equal:
                return "="
            case TermModifierOperator.Greater:
                return ">"

class Rule(ABC):
    pass

class Null(Rule):
    def __str__(self) -> str:
        return f"-"

class Term(Rule):
    term: str
    modifier: Optional[tuple[TermModifierOperator, str]]

    def __init__(self, term: str, modifier: Optional[tuple[TermModifierOperator, str]] = None):
        self.term = term
        self.modifier = modifier

    def __str__(self) -> str:
        if self.modifier is None:
            return self.term
        print(f"{self.modifier[0]}")
        return f"{self.term}{self.modifier[0]}{self.modifier[1]}"

class Group(Rule):
    rule: "Rule"

    def __init__(self, rule: Rule = Null()):
        self.rule = rule

    def __str__(self):
        return f"({self.rule})"

class Disjunction(Rule):
    a: "Rule"
    b: "Rule"

    def __init__(self, a: Rule = Null(), b: Rule = Null()):
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f"{self.a} | {self.b}"

class Conjunction(Rule):
    a: "Rule"
    b: "Rule"

    def __init__(self, a: Rule = Null(), b: Rule = Null()):
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f"{self.a} + {self.b}"
