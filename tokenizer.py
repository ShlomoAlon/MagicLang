from __future__ import annotations
import re
from Types import *
from typing import *

class Tokens:
    tokens: list[str]
    cur: int

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.cur = 0

    def next(self) -> str | None:
        if self.cur >= len(self.tokens):
            return None
        else:
            self.cur += 1
            return self.tokens[self.cur - 1]

    def peek(self) -> str | None:
        if self.cur >= len(self.tokens):
            return None
        else:
            return self.tokens[self.cur]

    def __repr__(self):
        return self.tokens[self.cur:].__repr__()

    def __bool__(self):
        if self.cur >= len(self.tokens):
            return False
        else:
            return True

    @staticmethod
    def tokenize(text: str) -> Tokens:
        # Updated regex pattern to handle more token types
        pattern = r'( |\n|\\|\||"[^"]*"|[0-9]+(?:\.[0-9]+)?|[^()\\ \n"|]+|\(|\))'
        tokens = [t for t in re.findall(pattern, text) if t]  # Remove empty matches
        return Tokens(tokens)

