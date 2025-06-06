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
        return Tokens(result)



def test_tokenize():
    tokens = Tokens.tokenize("hello | world \n (print)")
    assert tokens.tokens == ['hello', ' ', '|', ' ', 'world', ' ', '\n', ' ', '(', 'print', ')']



