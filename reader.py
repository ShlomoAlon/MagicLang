from __future__ import annotations
from typing import *
from Types import *
from tokenizer import Tokens

def parse_if(tokens: Tokens) -> PipeListType:
    assert tokens.next() == "if"
    ast = PipeListType()
    ast.append("'if")

    ast.append(parse_block(tokens, ends=["then"]))
    assert tokens.next() == "then"
    ast.append(parse_block(tokens, ends=["else", "end_if"]))
    assert tokens.peek() in ["else", "end_if"]
    if tokens.peek() == "else":
        tokens.next()  # consume 'else'
        ast.append(parse_block(tokens, ends=["end_if"]))
    assert tokens.next() == "end_if"
    return ast

def parse_filter(tokens: Tokens) -> LineList:
    assert tokens.next() == "filter"
    ast = LineList()
    ast.append("'filter")
    
    # Parse the filter predicate as a pipeline
    ast.append(parse_block(tokens, ends=["end_filter"]))
    assert tokens.next() == "end_filter"
    return ast


def parse(text: str) -> PipeListType:
    tokens = Tokens.tokenize(text)
    return parse_block(tokens)

def parse_block(tokens: Tokens, ends: list[str] = ()) -> PipeListType:
    ast = PipeListType()
    while tokens and tokens.peek() not in ends:
        ast.append(parse_line(tokens, ends))
    
    return ast

def parse_line(tokens: Tokens, ends: list[str]) -> LineList | Literal["Empty"]:
    new_lines = ('|', '\n')
    
    # Handle empty lines or pure newlines
    if not tokens or tokens.peek() in new_lines:
        while tokens and tokens.peek() in new_lines:
            tokens.next()
        return "Empty"

    ast = LineList()
    while tokens and tokens.peek() not in new_lines and tokens.peek() not in ends:
        if len(ast) == 0:
            if tokens.peek() == "filter":
                ast = parse_filter(tokens)
                break

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
    elif token == "if":
        return parse_if(tokens)

    elif token == "true":
        return True
    elif token == "false":
        return False

    elif token in ["then", "else", "end_if", "end_filter"]:
        raise SyntaxError(f"Unexpected keyword {token}")
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
    expected = "(seq 0 10 | 'filter (mod 5 | eq 0 | or (item | mod 3 | eq 0)) | sum | print\n\n23)"
    result = value_string(ast)
    assert result == expected
    print("\nParse tree representation:")
    print(result)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}" 