from _ast import While

from Types import Environment
from Types import *
from typing import *


def eval_ast(ast: Any, env: Environment, value: any = None) -> any:
    from Types import value_string
    print(f"EVAL: evaluating ast: {value_string(ast)} type {type(ast)} with {value and value_string(value)}")
    result = None
    if isinstance(ast, str):
        if ast.startswith('"'):
            result = ast
        else:
            result = env.get(ast)

    elif isinstance(ast, PipeListType):
        # Handle pipeline operations
        result = value
        for item in ast:
            result = eval_ast(item, env, result)
            
    elif isinstance(ast, LineList):
        if len(ast) == 0:
            result = None
        else:
            func = eval_ast(ast[0], env)
            if len(ast) == 1 and value is None and not callable(func):
                result = func
            else:
                args = ast[1:]

                if isinstance(func, Function):
                    result = func(env, args, value)

                elif isinstance(func, str):
                    # maybe the symbol is a method of the object value
                    if hasattr(value, func):
                        getattr(func, value)(*[eval_ast(new_ast, env) for new_ast in args])
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

    print(f"EVAL: Evaluated {value_string(ast)} with {value and value_string(value)} got {result and value_string(result)}")

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
    from Types import value_string
    with open("examples/euler1.magic", 'r') as f:
        content = f.read()
    ast = parse(content)
    print("PARSE: Parse tree representation:")
    print(value_string(ast))
    
    env = create_default_env()
    result = eval_ast(ast, env)
    print("RESULT: Evaluation result:")
    print(value_string(result))
    assert value_string(result) == "23"

