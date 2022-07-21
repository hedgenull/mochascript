from ast import Not

from common import *

OP_TO_FUNC_MAP = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "%": "mod",
}


class BaseObject:
    """Base class for all objects in the language."""

    def repr(self):
        return str(self.value)

    def type(self):
        return self.__class__.__name__


class Number(BaseObject):
    """Number class for the language."""

    def __init__(self, value):
        self.value = float(value)

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        elif isinstance(other, BinOp):
            return self.add(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        elif isinstance(other, BinOp):
            return self.sub(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        elif isinstance(other, BinOp):
            return self.mul(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def div(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        elif isinstance(other, BinOp):
            return self.div(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        elif isinstance(other, BinOp):
            return self.mod(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def visit(self):
        return self

    def repr(self):
        return str(self.value).strip(".0") if self.value % 1 == 0 else str(self.value)


class String(BaseObject):
    """String class for the language."""

    def __init__(self, value):
        self.value = str(value).strip("\"'")

    def add(self, other):
        if isinstance(other, BinOp):
            return self.add(other.visit())
        else:
            return String(self.value + other.repr())

    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value)
        elif isinstance(other, BinOp):
            return self.mul(other.visit())
        else:
            abort(f"Invalid types for operation: String and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, BinOp):
            return self.mod(other.visit())
        else:
            return String(self.value.replace("{}", other.repr()))

    def visit(self):
        return self


class BinOp(BaseObject):
    """Binary operation class for the language."""

    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def add(self, other):
        return self.visit().add(other)

    def sub(self, other):
        return self.visit().sub(other)

    def mul(self, other):
        return self.visit().mul(other)

    def div(self, other):
        return self.visit().div(other)

    def mod(self, other):
        return self.visit().mod(other)

    def visit(self):
        return eval(f"self.right.{OP_TO_FUNC_MAP[self.op]}(self.left)")

    def repr(self):
        return self.visit().repr()


class Function(BinOp):
    """Base function class for the language. Inherits from BinOp because of mathematical operations, which work the same as BinOp's do."""

    def repr(self):
        return f"<function {self.__class__.__name__}>"


class BuiltInFunction(Function):
    """Base class for built-in functions."""

    def repr(self):
        return f"<built-in function {self.__class__.__name__}>"


class Print(Function):
    """Print function."""

    def __init__(self, expr):
        self.expr = expr
        self.result = expr.visit()

    def visit(self):
        print(self.result.repr())
        return self.expr
