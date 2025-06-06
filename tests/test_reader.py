import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from reader import parse
from Types import value_string


@pytest.mark.parametrize('src', [
    '1 2 | 3',
    'eq 0 | or (item | mod 3 | eq 0)',
])
def test_roundtrip_simple(src):
    ast = parse(src)
    assert parse(value_string(ast)) == ast


def test_roundtrip_example_file():
    with open('examples/euler1.magic') as f:
        src = f.read()
    ast = parse(src)
    assert parse(value_string(ast)) == ast


def test_empty_line_roundtrip():
    src = "1\n\n2"
    ast = parse(src)
    assert len(ast) == 3
    assert isinstance(ast[1], list) and len(ast[1]) == 0
    assert parse(value_string(ast)) == ast


def test_roundtrip_nontrivial_program():
    src = (
        "seq 1 10\n"
        "filter (eq 5)\n"
        "get 0\n"
        "save five\n\n"
        "for (i) (seq 0 five) (\n"
        "echo i\n\n"
        "i | + 2 | echo\n"
        ")"
    )
    ast = parse(src)
    assert parse(value_string(ast)) == ast

