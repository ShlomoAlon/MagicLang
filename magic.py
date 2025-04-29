from reader import parse
from eval import eval_ast, create_default_env
from Types import *
import pytest

def run_magic_file(filename: str) -> str:
    """
    Reads and executes a magic file, returning its output.
    Captures print output for testing purposes.
    """
    with open(filename, 'r') as f:
        content = f.read()
    
    # Parse and evaluate
    ast = parse(content)
    print(ast.value_string())
    print("AST:", type(ast))
    print("AST value:", [type(x) for x in ast.value])
    if ast.value:
        print("First line value:", [type(x) for x in ast.value[0].value] if isinstance(ast.value[0], ListType) else type(ast.value[0]))
    env = create_default_env()
    
    # Capture print output
    import io
    import sys
    output = io.StringIO()
    sys.stdout = output
    
    # Evaluate
    eval_ast(ast, env)
    
    # Restore stdout and get output
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

def main():
    # Run euler1.magic and print its contents and output
    filename = "examples/euler1.magic"
    
    # Print file contents
    with open(filename, 'r') as f:
        print(f.read())
    
    # Run and print output
    output = run_magic_file(filename)
    print(output)

# Tests
def test_euler1():
    output = run_magic_file("examples/euler1.magic")
    assert output == "23", f"Expected 23, got {output}"

if __name__ == "__main__":
    main() 