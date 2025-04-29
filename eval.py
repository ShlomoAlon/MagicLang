from Types import *
from typing import *
from reader import parse

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
            if isinstance(func, Function):
                result = func(env, args, value)
            if callable(func):
                if value is not None:
                    raise TypeError("built in functions can't read from input")
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
    env = Environment()


    env.set(
        "seq", range
    )
    def magic_if(arg1, arg2, arg3):
        if arg1:
            return arg2
        else:
            return arg3
    env.set("magic_if", magic_if)

    env.set("magic_and", lambda arg1, arg2: arg1 and arg2)
    env.set("magic_or", lambda arg1, arg2: arg1 or arg2)

    env.set("magic_for", lambda arg1, arg2: arg1 or arg2)


    env.set(
        "'filter", magic_filter
    )
    return env

def test_euler1_eval():
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