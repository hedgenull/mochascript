import re
from calendar import c
from random import randint

from utils import *

BINOP_TO_FUNC_MAP = {
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
    "&&": "_and",
    "||": "_or",
}

UNOP_TO_FUNC_MAP = {
    "+": "pos",
    "-": "neg",
}


class BaseObject:
    """Base class for all objects in the language."""

    def add(self, other):
        return self.visit().add(other.visit())

    def sub(self, other):
        return self.visit().sub(other.visit())

    def mul(self, other):
        return self.visit().mul(other.visit())

    def div(self, other):
        return self.visit().div(other.visit())

    def mod(self, other):
        return self.visit().mod(other.visit())

    def lt(self, other):
        return Boolean(self.visit().value < other.visit().value)

    def gt(self, other):
        return Boolean(self.visit().value > other.visit().value)

    def le(self, other):
        return Boolean(self.visit().value <= other.visit().value)

    def ge(self, other):
        return Boolean(self.visit().value >= other.visit().value)

    def eq(self, other):
        return Boolean(self.visit().value == other.visit().value)

    def ne(self, other):
        return Boolean(self.visit().value != other.visit().value)

    def pos(self):
        return +self.value

    def neg(self):
        return -self.value

    def _and(self, other):
        return Boolean(Boolean(self.visit().value).value and Boolean(other.visit().value).value)

    def _or(self, other):
        return Boolean(Boolean(self.visit().value).value or Boolean(other.visit().value).value)

    def visit(self):
        return self

    def repr(self):
        return str(self.value)

    def type(self):
        return self.__class__.__name__


class Atom(BaseObject):
    """Base class for all atoms- i.e. objects that have a "value" attribute"""


class Number(Atom):
    """Number class for the language."""

    def __init__(self, value):
        self.value = float(value)

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        elif isinstance(other, SpecialExpression):
            return self.add(other.visit())
        abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        elif isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        elif isinstance(other, SpecialExpression):
            return self.mul(other.visit())
        abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def div(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        elif isinstance(other, SpecialExpression):
            return self.div(other.visit())
        abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        elif isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def pos(self):
        return Number(+self.value)

    def neg(self):
        return Number(-self.value)

    def repr(self):
        return (
            (str(self.value).strip(".0") if self.value % 1 == 0 else str(self.value))
            if self.value
            else "0"
        )


class String(Atom):
    """String class for the language."""

    def __init__(self, value=""):
        self.value = (
            str(value).strip("\"'").replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")
        )

    def add(self, other):
        if isinstance(other, SpecialExpression):
            return self.add(other.visit())
        return String(self.value + other.repr())

    def sub(self, other):
        if isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        return String(self.value.replace(other.repr(), ""))

    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * int(other.value))
        elif isinstance(other, SpecialExpression):
            return self.mul(int(other.visit()))
        abort(f"Invalid types for operation: String and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        return String(self.value.replace("{}", other.repr()))


class Array(Atom):
    """Array/list class for the language."""

    def __init__(self, values):
        self.values = [value.visit() for value in values]

    def add(self, other):
        if isinstance(other, Array):
            return Array(self.values.extend(other.values))
        elif isinstance(other, Atom):
            return Array(self.values + [other.visit()])
        elif isinstance(other, SpecialExpression):
            return self.add(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def sub(self, other):
        if isinstance(other, Atom):
            copy = self.values[:]
            while other in copy:
                copy.remove(other)
            return Array(copy)
        elif isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def mul(self, other):
        if isinstance(other, Number):
            return Array(self.values * other.value)
        elif isinstance(other, SpecialExpression):
            return self.mul(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, Number):
            return self.values[int(other.value)]
        elif isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def neg(self):
        return Array(self.values[::-1])

    def repr(self):
        return f"[{', '.join((value.repr() for value in self.values))}]"


class Boolean(Atom):
    """Boolean class for the language."""

    def __init__(self, value=True):
        self.value = bool(value)

    def repr(self):
        return str(self.value).lower()


class Null(Atom):
    """Null, None, void, nil, whatever you want to call it."""

    def __init__(self):
        self.value = None

    def repr(self):
        return "null"


class SpecialExpression(BaseObject):
    pass


class BinOp(SpecialExpression):
    """Binary operation class for the language."""

    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def visit(self):
        return eval(f"self.right.{BINOP_TO_FUNC_MAP[self.op]}(self.left)")

    def repr(self):
        return self.visit().repr()


class UnOp(SpecialExpression):
    """Unary operation class for the language."""

    def __init__(self, op, value):
        self.op = op
        self.value = value

    def visit(self):
        return eval(f"self.value.{UNOP_TO_FUNC_MAP[self.op]}()")


class IfExpression(SpecialExpression):
    """If-expression class for the language."""

    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def visit(self):
        return (
            self.true_block.visit()
            if self.condition.visit().value == True
            else self.false_block.visit()
        )


class ForExpression(SpecialExpression):
    """For-loop expression for the language."""

    def __init__(self, iname, ival, toval, block):
        self.iname = iname
        self.ival = ival
        self.toval = toval
        self.block = block
        Assignment(self.iname, self.ival).visit()

    def visit(self):
        while ENV[-1][self.iname] != self.toval:
            self.ival += 1
            Assignment(self.iname, self.ival).visit()
            self.block.visit()

        return self.block.visit()


class Assignment(SpecialExpression):
    """Assignment manager for the language."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def visit(self):
        ENV[-1][self.name] = self.value.visit()
        return ENV[-1][self.name]


class Variable(SpecialExpression):
    """Variable manager for the language."""

    def __init__(self, name):
        self.name = name

    def visit(self):
        value = ENV[-1].get(self.name)
        if not value:
            abort(f"Undefined variable {self.name}")
        return value


class SayNode(SpecialExpression):
    """It says the expression."""

    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        result = self.expr.visit()
        print(result.repr())
        return result


class AskNode(SpecialExpression):
    """Get user input."""

    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return String(input(self.expr.visit().repr()))


class ExitNode(SpecialExpression):
    """It says the expression, and then exits."""

    def __init__(self, expr=String()):
        self.expr = expr

    def visit(self):
        abort(self.expr.visit().repr())


class BlockNode(SpecialExpression):
    """Multiple lines of code."""

    def __init__(self, *exprs):
        self.exprs = exprs

    def visit(self):
        return [expr.visit() for expr in self.exprs][-1]


class Env(dict):
    """Environment object. Used to store variables."""

    def __init__(self, **kwargs):
        self.constants = []
        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, key, value):
        if key in self.constants:
            return
        elif key.startswith("CONST_"):
            self.constants.append(key.removeprefix("CONST_"))
        super().__setitem__(key.removeprefix("CONST_"), value)

    def __getitem__(self, key):
        return super().__getitem__(key)


ENV = [
    Env(
        **{
            # Built-in functions:
            # ...
            # Special constants:
            "CONST_true": Boolean(True),
            "CONST_yes": Boolean(True),
            "CONST_false": Boolean(False),
            "CONST_no": Boolean(False),
            "CONST_null": Null(),
        }
    ),
]
