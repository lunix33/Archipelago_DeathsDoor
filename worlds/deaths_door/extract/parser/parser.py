from typing import Optional

from . import rule
from .token import Token, TokenType
from .lexer import Lexer

class Parser:
    definitions: list[rule.TermDefinition]
    nullified: set[str]
    lexer: Lexer

    # State
    isStateless: bool = False
    stack: list["rule.Rule"] = []
    activeTerm: Optional[rule.TermDefinition] = None

    def __init__(self, lexer: Lexer, nullified: set[str] = set()) -> None:
        self.definitions = []
        self.nullified = nullified
        self.lexer = lexer

    def _finalize_token(self):
        if self.activeTerm is None:
            raise Exception("No term to finalize")

        if len(self.stack) == 0:
            raise Exception("No item in the token stack.")
        elif len(self.stack) > 1:
            raise Exception(f"Too many terms in the stack: {"->".join(map(lambda i: str(i),self.stack))}")

        self.activeTerm.rule = self.stack[0]
        self.definitions.append(self.activeTerm)

        self.isStateless = False
        self.activeTerm = None
        self.stack = []

    def _set_term_definition(self, term: Token):
        self.activeTerm = rule.TermDefinition(self.isStateless, term.value)
        self.stack = [rule.Null()]

    def _open_group(self):
        if isinstance(self.stack[-1], rule.Term):
            raise Exception(f"Group can't follow a term.")
        self.stack.append(rule.Group())
        self.stack.append(rule.Null())

    def _close_group(self):
        stack_rule = self.stack.pop()
        group = self.stack.pop()
        previous = self.stack.pop()

        if not isinstance(group, rule.Group):
            raise Exception(f"Did not find the closing group, found: {group} with {stack_rule} for {previous}")
        group.rule = stack_rule

        if isinstance(previous, (rule.Conjunction, rule.Disjunction)):
            previous.b = group
        elif isinstance(previous, rule.Group):
            previous.rule = group
        elif isinstance(previous, rule.Null):
            previous = group
        
        self.stack.append(previous)

    def _handle_term(self, token: Token):
        if token.value in self.nullified:
            term = rule.Null()
        elif token.value == "NONE":
            term = rule.Boolean(False)
        else:
            term = rule.Term(token.value)
        previous = self.stack.pop()

        if isinstance(previous, rule.Term):
            raise Exception(f"Found a term following another term: {previous} followed by {term}")

        if isinstance(previous, (rule.Conjunction, rule.Disjunction)):
            previous.b = term
        elif isinstance(previous, rule.Group):
            previous.rule = term
        elif isinstance(previous, rule.Null):
            previous = term

        self.stack.append(previous)

    def _handle_term_modifier(self, token: Token):
        previous = self.stack.pop()

        term = previous
        while not isinstance(term, rule.Term):
            if isinstance(term, (rule.Conjunction, rule.Disjunction)):
                term = term.b
            elif isinstance(term, rule.Group):
                term = term.rule
            else:
                raise Exception(f"Was not able to find term for modifier: {token}")

        if token.ttype is TokenType.StateEqual:
            term.modifier = (rule.TermModifierOperator.Equal, token.value)
        elif token.ttype is TokenType.StateGreater:
            term.modifier = (rule.TermModifierOperator.Greater, token.value)

        self.stack.append(previous)

    def _handle_operator(self, token: Token):
        previous = self.stack.pop()

        if token.ttype is TokenType.Conjonction:
            self.stack.append(rule.Conjunction(previous))
        elif token.ttype is TokenType.Disjonction:
            self.stack.append(rule.Disjunction(previous))
        else:
            raise Exception(f"Found invalid token: {token}")

    def _out_of_definition(self, token: Token):
        # Invalid state
        if token.ttype not in [TokenType.Stateless, TokenType.TermDef]:
            raise Exception(f"Failed to parse token: {token}")

        # Upcoming term definition is stateless
        if token.ttype is TokenType.Stateless:
            self.isStateless = True

        # Set active term definition.
        elif token.ttype is TokenType.TermDef:
            self._set_term_definition(token)

    def _in_of_definition(self, token: Token):
        # Finalize a term definition is active
        if token.ttype in [TokenType.Stateless, TokenType.TermDef]:
            self._finalize_token()
            self._out_of_definition(token)

        # Handle operator
        elif (token.ttype in [TokenType.Conjonction, TokenType.Disjonction]):
            self._handle_operator(token)
             
        # Handle rule groups
        elif token.ttype is TokenType.OpenParent:
            self._open_group()
        elif token.ttype is TokenType.CloseParent:
            self._close_group()

        # Handle terms
        elif token.ttype is TokenType.Term:
            self._handle_term(token)

        elif token.ttype in [TokenType.StateEqual, TokenType.StateGreater]:
            self._handle_term_modifier(token)

        else:
            raise Exception(f"Invalid token found: {token}")

    def parse(self) -> list[rule.TermDefinition]:
        for t in self.lexer.tokens():
            if t is None:
                break

            if self.activeTerm is not None:
                self._in_of_definition(t)
            else:
                self._out_of_definition(t)

        self._finalize_token()

        return self.definitions
