import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tokenizer import Tokens


def test_tokenize_basic():
    text = "hello | world \n (print)"
    tokens = Tokens.tokenize(text)
    assert tokens.tokens == ['hello', ' ', '|', ' ', 'world', ' ', '\n', ' ', '(', 'print', ')']


def test_tokenize_nontrivial_program():
    text = (
        "seq 1 10\n"
        "filter (eq 5)\n"
        "get 0\n"
        "save five\n\n"
        "for (i) (seq 0 five) (\n"
        "echo i\n\n"
        "i | + 2 | echo\n"
        ")"
    )
    tokens = Tokens.tokenize(text)
    assert tokens.tokens == [
        'seq', ' ', '1', ' ', '10', '\n', 'filter', ' ', '(', 'eq', ' ', '5', ')', '\n',
        'get', ' ', '0', '\n', 'save', ' ', 'five', '\n', '\n', 'for', ' ', '(', 'i', ')',
        ' ', '(', 'seq', ' ', '0', ' ', 'five', ')', ' ', '(', '\n', 'echo', ' ', 'i',
        '\n', '\n', 'i', ' ', '|', ' ', '+', ' ', '2', ' ', '|', ' ', 'echo', '\n', ')'
    ]

