from __future__ import annotations

import typing
from typing import *

from eval import eval_ast

if typing.TYPE_CHECKING:
    from typing import *
class Function:
    def __call__(self, env: Environment, args, in_value):
        raise NotImplementedError()

class UserFunction(Function):
    pipe: PipeListType
    def __init__(self, pipe_line: PipeListType):
        self.pipe = pipe_line

    def __call__(self, env: Environment, args, in_value):
        class NewEnv(type(env)):
            def get(self, name: str) -> Any:
                if name.startswith("@"):
                    return eval_ast(args[int(name[1:])], env)
                elif name.startswith("$"):
                    return args[int(name[1:])]
                else:
                    return super().get(name)

class While(Function):
    def __call__(self, env: Environment, args, in_value):
        assert in_value is None
        while eval_ast(args[0], env):
            eval_ast(args[1], env)

class IfFunction(Function):
    def __call__(self, env: Environment, args, in_value):
        assert in_value is None
        if eval_ast(args[0], env):
            return eval_ast(args[1], env)
        elif len(args) == 3:
            return eval_ast(args[2], env)
        else:
            return None

class And(Function):
    def __call__(self, env: Environment, args, in_value):
        cur = in_value or True
        index = 0
        while cur and index < len(args):
            cur = eval_ast(args[index], env)
            index += 1
        return cur

class Or(Function):
    def __call__(self, env: Environment, args, in_value):
        cur = in_value or False
        index = 0
        while not cur and index < len(args):
            cur = eval_ast(args[index], env)
            index += 1
        return cur

class Save(Function):
    def __call__(self, env: Environment, args, in_value):
        if in_value:
            assert len(args) == 1
            env.set(eval_ast(args[0], env), in_value)
            return in_value
        else:
            assert len(args) == 2
            value = eval_ast(args[1], env)
            env.set(eval_ast(args[0], env), value)
            return value

class Filter(Function):
    def __call__(self, env: Environment, args, in_value):
        filter()






