from _ast import While
from readline import set_completion_display_matches_hook

from Types import Environment
from Types import *
from typing import *


def eval_ast(ast: Any, env: Environment, value: any = None) -> any:
    print(f"evaluating ast: {ast.value_string()} type {type(ast)} with {value and value.value_string()}")
    result = None
    if isinstance(ast, str):
        if ast.startswith('"'):
            result = ast
        else:
            result = env.get(ast)

    elif isinstance(ast, PipeListType):
        # Handle pipeline operations
        current_value = value
        for item in ast:
            if item == "Empty":
                current_value = None
            else:
                current_value = eval_ast(item, env, current_value)
            
        result = current_value
    elif isinstance(ast, LineList):
        assert len(ast) != 0
        # First element should be a function or special form
        func = eval_ast(ast[0], env)
        if len(ast) == 1:
            result = func
        else:
            args = ast[1:]
            # the function is a built int function defined in magic lang itself
            if isinstance(func, Function):
                result = func(env, args, value)
            elif isinstance(func, str):
                # maybe the symbol is a method of the object value
                hasattr(value, func) and getattr(func, value)(*[eval_ast(new_ast, env) for new_ast in args])
            # the function is a built-in python function
            elif callable(func):
                if value is not None and len(args) > 0:
                    raise TypeError("built in functions can't be in the middle of a pipeline")
                if value is not None and len(args) == 0:
                    result = func(value)
                result = func(*[eval_ast(new_ast, env) for new_ast in args])
            else:
                raise TypeError(f"Cannot call {func} current ast is {value_string(ast)}")

    # Numbers, booleans, and strings evaluate to themselves
    elif isinstance(ast, (int, float)):
        return ast
    else:
        raise TypeError(f"Cannot evaluate {ast}")

    print(f"Evaluated {value_string(ast)} with {value and value_string(value)} got {result and value_string(result)}")

    return result



def create_default_env() -> Environment:
    from functions import And, Or, While
    env = Environment()


    env.set(
        "seq", range
    )


    env.set("and", And)
    env.set("or", Or)
    env.set("==", "__eq__")
    env.set("next", "__next__")
    env.set("<", "__lt__")
    env.set("<=", "__le__")
    env.set(">", "__gt__")
    env.set(">=", "__ge__")
    env.set("while", While)
    env.set("sum", sum)

    return env

def test_euler1_eval():
    from reader import parse
    with open("examples/euler1.magic", 'r') as f:
        content = f.read()
    ast = parse(content)
    print("\nParse tree representation:")
    print(ast.value_string())
    
    env = create_default_env()
    result = eval_ast(ast, env)
    print("\nEvaluation result:")
    print(result.value_string())
    assert result.value_string() == "23" 