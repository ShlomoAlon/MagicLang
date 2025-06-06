from __future__ import annotations
import re
from Types import *
from typing import *

class Tokens:
    """Simple loss‑less token stream."""

    tokens: list[str]
    cur: int

    def __init__(self, tokens: list[str]) -> None:
        # Store the list of tokens and initialise the cursor.
        self.tokens = tokens
        self.cur = 0

    def next(self) -> str | None:
        """Return and consume the next token or ``None`` if exhausted."""
        if self.cur >= len(self.tokens):
            return None
        else:
            self.cur += 1
            return self.tokens[self.cur - 1]

    def peek(self) -> str | None:
        """Look at the upcoming token without consuming it."""
        if self.cur >= len(self.tokens):
            return None
        else:
            return self.tokens[self.cur]

    def __repr__(self):
        """Debug representation showing remaining tokens."""
        return self.tokens[self.cur:].__repr__()

    def __bool__(self):
        """Boolean context: ``False`` when all tokens were consumed."""
        if self.cur >= len(self.tokens):
            return False
        else:
            return True

    @staticmethod
    def tokenize(text: str) -> Tokens:
        """Tokenise ``text`` according to the separator rules in spec.md."""
        result = []
        builder = ""
        for i in text:
            if i in "()\{}[];:| \n":
                if builder != "":
                    result.append(builder)
                    builder = ""
                result.append(i)
            else:
                builder += i
        if builder:
            result.append(builder)
        return Tokens(result)



def test_tokenize():
    tokens = Tokens.tokenize("hello | world \n (print)")
    assert tokens.tokens == ['hello', ' ', '|', ' ', 'world', ' ', '\n', ' ', '(', 'print', ')']



