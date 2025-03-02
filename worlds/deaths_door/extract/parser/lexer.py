from collections.abc import Callable, Generator
from typing import Optional, Self

from .token import Token, TokenType

type CheckFn[T] = Callable[[T], tuple[int, Optional[Token]]]

class Lexer:
    content: str
    position: int

    def __init__(self, content: str):
        self.content = content
        self.position = 0

    def tokens(self) -> Generator[Optional[Token]]:
        while self.position < len(self.content):
            yield self._runRules()

    @classmethod
    def mod_simple(cls, expected: str, ttype: TokenType) -> CheckFn[Self]:
        def simple(s: Self) -> tuple[int, Optional[Token]]:
            chars = s.content[s.position:s.position + len(expected)]
            if chars == expected:
                return len(expected), Token(ttype, chars)
            return 0, None
        return simple

    @classmethod
    def mod_termParse(cls) -> CheckFn[Self]:
        def termParse(s: Self) -> tuple[int, Optional[Token]]:
            start = s.position
            end = s.position

            char = s.content[end]
            while char.isalnum() or (char in ["$", "_", "[", "]", "'", "-"]):
                end += 1
                if end == len(s.content):
                    break
                char = s.content[end]
            
            step = (end - start)
            if step == 0:
                return step, None

            if end < len(s.content) and s.content[end] == ":":
                return step + 1, Token(TokenType.TermDef, s.content[start:end])
            else:
                return step, Token(TokenType.Term, s.content[start:end])
        return termParse

    @classmethod
    def mod_stateModifierParse(cls) -> CheckFn[Self]:
        def stateModifierParse(s: Self) -> tuple[int, Optional[Token]]:
            start = s.position
            end = s.position + 1

            char = s.content[start]
            ttype = TokenType.Illegal
            if char == ">":
                ttype = TokenType.StateGreater
            elif char == "=":
                ttype = TokenType.StateEqual

            if ttype is TokenType.Illegal:
                return 0, None
            
            char = s.content[end]
            while char.isalnum():
                end += 1
                if end == len(s.content):
                    break
                char = s.content[end]

            step = (end - start)
            return step, Token(ttype, s.content[start + 1:end])
        return stateModifierParse
    
    @classmethod
    def mod_commentParse(cls) -> CheckFn[Self]:
        def commentParse(s: Self) -> tuple[int, Optional[Token]]:
            initial = s.content[s.position:s.position + 2]
            if initial != "//":
                return 0, None

            start = s.position + 3
            end = start
            char = s.content[end]

            while char != "\n":
                end += 1
                char = s.content[end]

            step = (end - start) + 3
            return step, Token(TokenType.Comment, s.content[start:end].strip())
        return commentParse
    
    @classmethod
    def mod_whitespaceParse(cls) -> CheckFn[Self]:
        def whitespaceParse(s: Self) -> tuple[int, Optional[Token]]:
            start = s.position
            end = start
            while s.content[end].isspace():
                end += 1
                if end == len(s.content):
                    break
            
            step = (end - start)
            if step == 0:
                return 0, None
            return step, Token(TokenType.Whitespace, "")
        return whitespaceParse

    def _runRules(self) -> Optional[Token]:
        if self.position == len(self.content):
            return None

        for r in RULES:
            step, t = r(self)
            if t is not None:
                self.position += step
                if (t.ttype in [TokenType.Whitespace, TokenType.Comment, TokenType.StateWarn]):
                    return self._runRules()
                return t

        self.position += 1
        return Token(TokenType.Illegal, self.content[self.position - 1])

RULES: list[CheckFn[Lexer]] = [
    Lexer.mod_whitespaceParse(),
    Lexer.mod_commentParse(),
    Lexer.mod_simple("/", TokenType.StateWarn),
    Lexer.mod_simple("+", TokenType.Conjonction),
    Lexer.mod_simple("|", TokenType.Disjonction),
    Lexer.mod_stateModifierParse(),
    Lexer.mod_simple("(", TokenType.OpenParent),
    Lexer.mod_simple(")", TokenType.CloseParent),
    Lexer.mod_simple("stateless", TokenType.Stateless),
    Lexer.mod_termParse(),
]

