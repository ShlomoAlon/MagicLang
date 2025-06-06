from __future__ import annotations

import textwrap
from typing import *

def value_string(value: LineList | PipeListType | object, nested=0) -> str:

    if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, LineList):
        return " ".join([value_string(value, nested=nested + 1) for value in value])
    elif isinstance(value, PipeListType):
        parts = [value_string(v, nested=nested) for v in value]
        inner = "\n".join(parts)
        if nested == 0:
            return inner
        else:
            return f"({inner})"
    else:
        raise TypeError(f"Unsupported type {type(value)}")

class LineList(List):
    pass


class PipeListType(List):
    pass

class Function:
    def __call__(self, env: Environment, args, in_value):
        raise NotImplementedError()














#
# TokenizedPrimitives = int | float | str
# AllPrimitives = TokenizedPrimitives | bool | None



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




