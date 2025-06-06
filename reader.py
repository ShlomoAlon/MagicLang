from __future__ import annotations
from typing import *
from Types import PipeListType, LineList
from tokenizer import Tokens



def parse(text: str) -> PipeListType:
    tokens = Tokens.tokenize(text)
    return parse_block(tokens)

def parse_block(tokens: Tokens, ends: list[str] = ()) -> PipeListType:
    ast = PipeListType()
    while tokens and tokens.peek() not in ends:
        ast.append(parse_line(tokens, ends))
    
    return ast

def parse_line(tokens: Tokens, ends: list[str]) -> LineList:
    new_lines = ('|', '\n')

    if not tokens or tokens.peek() in new_lines:
        while tokens and tokens.peek() in new_lines:
            tokens.next()
        return LineList()

    ast = LineList()

    while tokens and tokens.peek() not in new_lines and tokens.peek() not in ends:
        atom = parse_atom(tokens)

        if atom is not None:
            ast.append(atom)
            
    # Consume trailing newline or pipe if present
    if tokens and tokens.peek() in new_lines:
        tokens.next()

    return ast

def parse_atom(tokens: Tokens) -> Any:
    if not tokens:
        return None
        
    token = tokens.peek()
    
    if token == "(":
        tokens.next()  # consume opening paren
        result = parse_block(tokens, ends=[")"])
        if not tokens or tokens.next() != ")":
            raise SyntaxError("Unclosed parenthesis")
        return result
    elif token == " ":
        tokens.next()  # consume whitespace
        return None

    elif token == "true":
        return True
    elif token == "false":
        return False
    else:
        token = tokens.next()
        # Try to convert to number if possible
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token

def test_euler1_parse_tree():
    with open("examples/euler1.magic", 'r') as f:
        content = f.read()
    ast = parse(content)
    expected = """seq 0 10
'filter (
  mod 5
  eq 0
  or (
      item
      mod 3
      eq 0
  )
)
sum
print

23"""
    from Types import value_string
    result = value_string(ast)
    print(result)
    if result != expected:
        print("\nExpected:\n" + expected)
        print("\nGot:\n" + result)
    assert result == expected
    print("\nParse tree representation:")
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"