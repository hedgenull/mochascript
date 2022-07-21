from lib2to3.pgen2.token import OP

from common import *

OP_TO_FUNC_MAP = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "%": "mod",
    "==": "eq",
    "!=": "ne",
    "<": "lt",
    ">": "gt",
    "<=": "le",
    ">=": "ge",
}


class BaseObject:
    """Base class for all objects in the language."""

    def __getattr__(self, name):
        """Some fun metaprogramming techniques for less code!"""
        if name in OP_TO_FUNC_MAP.values():
            return lambda other: eval(f"self.visit().{name}(other)")

    def eq(self, other):
        return Boolean(self.visit() == other.visit())

    def ne(self, other):
        return Boolean(self.visit() != other.visit())

    def visit(self):
        return self

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

    def eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value)
        elif isinstance(other, BinOp):
            return self.eq(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def ne(self, other):
        if isinstance(other, Number):
            return Boolean(self.value != other.value)
        elif isinstance(other, BinOp):
            return self.ne(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def lt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value)
        elif isinstance(other, BinOp):
            return self.lt(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def gt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value > other.value)
        elif isinstance(other, BinOp):
            return self.gt(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def le(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value)
        elif isinstance(other, BinOp):
            return self.le(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def ge(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value)
        elif isinstance(other, BinOp):
            return self.ge(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def repr(self):
        return str(self.value).strip(".0") if self.value % 1 == 0 else str(self.value)


class Boolean(BaseObject):
    """Boolean class for the language."""

    def __init__(self, value=True):
        self.value = value

    def repr(self):
        return str(self.value).lower()


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


class BinOp(BaseObject):
    """Binary operation class for the language."""

    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def visit(self):
        return eval(f"self.right.{OP_TO_FUNC_MAP[self.op]}(self.left)")

    def repr(self):
        return self.visit().repr()


class IfNode(BaseObject):
    """If-expression class for the language."""

    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def visit(self):
        return self.true_block.visit() if self.condition.visit().value == True else self.false_block.visit()


class Function(BaseObject):
    """Base function class for the language."""

    def repr(self):
        return f"<function {self.__class__.__name__}>"


class BuiltInFunction(Function):
    """Base class for built-in functions."""

    def repr(self):
        return f"<built-in function {self.__class__.__name__}>"


class Print(BuiltInFunction):
    """Print function."""

    def __init__(self, expr):
        self.expr = expr
        self.result = expr.visit()

    def visit(self):
        print(self.result.repr())
        return self.expr


class Input(BuiltInFunction):
    """Input function."""

    def __init__(self, expr):
        self.result = expr.visit()

    def visit(self):
        return String(input(self.result.repr()))
