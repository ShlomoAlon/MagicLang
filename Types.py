from __future__ import annotations
from typing import *

from eval import eval_ast


def value_string(value: LineList | PipeListType | object) -> str:
    if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, LineList):
        return " ".join(map(value_string, value))
    elif isinstance(value, PipeListType):
        if len(value) == 1:
            return value_string(value[0])
        else:
            rep = "("

            saw_empty = True
            for val in value:
                if val == "Empty":
                    rep += "\n\n"
                    saw_empty = True
                else:
                    if saw_empty:
                        rep += value_string(val)
                        saw_empty = False
                    else:
                        rep += f" | {value_string(val)}"
            rep += ")"
            return rep
    else:
        raise TypeError(f"Unsupported type {type(value)}")

class LineList(List):
    pass


class PipeListType(List):
    pass

class Function:
    def __call__(self, env: Environment, args, in_value):
        raise NotImplementedError()















TokenizedPrimitives = int | float | str
AllPrimitives = TokenizedPrimitives | bool | None


class Environment:
    env: dict[str, Any]
    parent: Environment
    def __init__(self, parent: Environment | None = None):
        self.parent = parent
        self.env = {}

    def get(self, name: str) -> Any:
        if name in self.env:
            return self.env[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return name

    def set(self, name: str, value: Any) -> None:
        self.env[name] = value




