from enum import StrEnum, auto

class TokenType(StrEnum):
    Stateless = auto()    # stateless
    Term = auto()         # [a-z\[\]]*
    TermDef = auto()      # [a-z\[\]]*:
    OpenParent = auto()   # (
    CloseParent = auto()  # )
    Conjonction = auto()  # +
    Disjonction = auto()  # |
    StateGreater = auto() # >
    StateEqual = auto()   # =
    _Comment = auto()     # // ... \n
    Illegal = auto()      # Anything else...
    _Whitespace = auto()  # Whitespaces (skipped)
    _StateWarn = auto()   # /

class Token:
    ttype: TokenType
    value: str

    def __init__(self, ttype: TokenType, value: str) -> None:
        self.ttype = ttype
        self.value = value

    def __str__(self) -> str:
        return f"{self.ttype} {{ {str.encode(self.value)} }}"

