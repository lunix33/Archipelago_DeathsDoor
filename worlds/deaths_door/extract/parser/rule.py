
from abc import ABC
from enum import StrEnum, auto
from json import JSONEncoder
from typing import Any, Optional

class RuleJsonSerializer(JSONEncoder):
    def default(self, o: Any):
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
                a = dict.get("a")
                b = dict.get("b")
                if a is None or not isinstance(a, Rule):
                    raise Exception("Failed to parse conjunction. Side A is invalid", dict)
                if b is None or not isinstance(b, Rule):
                    raise Exception("Failed to parse conjunction. Side B is invalid", dict)
                return Conjunction(a, b)

            case "disjunction":
                a = dict.get("a")
                b = dict.get("b")
                if a is None or not isinstance(a, Rule):
                    raise Exception("Failed to parse disjunction. Side A is invalid", dict)
                if b is None or not isinstance(b, Rule):
                    raise Exception("Failed to parse disjunction. Side B is invalid", dict)
                return Disjunction(a, b)

            case "group":
                rule = dict.get("rule")
                if rule is None or not isinstance(rule, Rule):
                    raise Exception("Failed to parse group. Rule is invalid", dict)
                return Group(rule)

            case "term":
                term = dict.get("term")
                if term is None or not isinstance(term, str):
                    raise Exception("Failed to parse term. Term is invalid", dict)
                return Term(term, dict.get("modifier"))

            case _:
                stateless = bool(dict.get("stateless") or False)
                term = dict.get("term")
                if term is None or not isinstance(term, str):
                    raise Exception("Failed to parse term definition. Term is invalid", dict)
                rule = dict.get("rule")
                if rule is None or not isinstance(rule, Rule):
                    raise Exception("Failed to parse term definition. Rule is invalid", dict)
                return TermDefinition(stateless, term, rule)

class TermDefinition:
    stateless: bool
    term: str
    rule: "Rule"

    def __init__(self, stateless: bool, term: str, rule: Optional["Rule"] = None) -> None:
        self.stateless = stateless
        self.term = term
        self.rule = rule or Null()

    def to_name(self) -> str:
        return self.term.replace("_", " ")
    
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

    def to_name(self) -> str:
        return self.term.replace("_", " ")

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
