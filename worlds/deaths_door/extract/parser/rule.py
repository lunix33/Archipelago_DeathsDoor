
from abc import ABC, abstractmethod
from enum import StrEnum, auto
from json import JSONDecoder, JSONEncoder
from typing import Optional

class RuleJsonSerializer(JSONEncoder):
    def default(self, o):
        obj_dict = o.__dict__
        if isinstance(o, Null):
            obj_dict["type"] = "null"
        if isinstance(o, Conjunction):
            obj_dict["type"] = "conjonction"
        if isinstance(o, Disjunction):
            obj_dict["type"] = "disjunction"
        if isinstance(o, Group):
            obj_dict["type"] = "group"
        if isinstance(o, Term):
            obj_dict["type"] = "term"
        return obj_dict

class TermDefinition:
    stateless: bool
    term: str
    rule: "Rule"

    def __init__(self, stateless: bool, term: str) -> None:
        self.stateless = stateless
        self.term = term
        self.rule = Null()
    
    def __str__(self) -> str:
        return f"{"stateless " if self.stateless else ""}{self.term.value}: {self.rule}"

class TermModifierOperator(StrEnum):
    Equal = auto()
    Greater = auto()

    def __str__(self):
        match self:
            case [TermModifierOperator.Equal]:
                return "="
            case [TermModifierOperator.Greater]:
                return ">"

class Rule(ABC):
    pass

class Null(Rule):
    def __str__(self) -> str:
        return f"-"

class Term(Rule):
    term: str
    modifier: Optional[tuple[TermModifierOperator, str]]

    def __init__(self, term: str):
        self.term = term
        self.modifier = None

    def __str__(self) -> str:
        if self.modifier is None:
            return self.term
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
