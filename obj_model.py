from random import randint

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

    def add(self, other):
        return self.visit().add(other.visit().value)

    def sub(self, other):
        return self.visit().sub(other.visit().value)

    def mul(self, other):
        return self.visit().mul(other.visit().value)

    def div(self, other):
        return self.visit().div(other.visit().value)

    def mod(self, other):
        return self.visit().mod(other.visit().value)

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
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        elif isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        elif isinstance(other, SpecialExpression):
            return self.mul(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def div(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        elif isinstance(other, SpecialExpression):
            return self.div(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        elif isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        else:
            abort(f"Invalid types for operation: Number and {type(other).__name__}")

    # def lt(self, other):
    #     if isinstance(other, Number):
    #         return Boolean(self.value < other.value)
    #     elif isinstance(other, UnInstantiable):
    #         return self.lt(other.visit())
    #     else:
    #         abort(f"Invalid types for operation: Number and {type(other).__name__}")

    # def gt(self, other):
    #     if isinstance(other, Number):
    #         return Boolean(self.value > other.value)
    #     elif isinstance(other, UnInstantiable):
    #         return self.gt(other.visit())
    #     else:
    #         abort(f"Invalid types for operation: Number and {type(other).__name__}")

    # def le(self, other):
    #     if isinstance(other, Number):
    #         return Boolean(self.value <= other.value)
    #     elif isinstance(other, UnInstantiable):
    #         return self.le(other.visit())
    #     else:
    #         abort(f"Invalid types for operation: Number and {type(other).__name__}")

    # def ge(self, other):
    #     if isinstance(other, Number):
    #         return Boolean(self.value >= other.value)
    #     elif isinstance(other, UnInstantiable):
    #         return self.ge(other.visit())
    #     else:
    #         abort(f"Invalid types for operation: Number and {type(other).__name__}")

    def repr(self):
        return str(self.value).strip(".0") if self.value % 1 == 0 else str(self.value)


class Boolean(Atom):
    """Boolean class for the language."""

    def __init__(self, value=True):
        self.value = value

    def repr(self):
        return str(self.value).lower()


class Null(Atom):
    """Null, None, void, nil, whatever you want to call it."""

    def __init__(self):
        self.value = None

    def repr(self):
        return "null"


class String(Atom):
    """String class for the language."""

    def __init__(self, value=""):
        self.value = str(value).strip("\"'")

    def add(self, other):
        if isinstance(other, SpecialExpression):
            return self.add(other.visit())
        else:
            return String(self.value + other.repr())

    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value)
        elif isinstance(other, SpecialExpression):
            return self.mul(other.visit())
        else:
            abort(f"Invalid types for operation: String and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        else:
            return String(self.value.replace("{}", other.repr()))


class SpecialExpression(BaseObject):
    pass


class BinOp(SpecialExpression):
    """Binary operation class for the language."""

    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def visit(self):
        return eval(f"self.right.{OP_TO_FUNC_MAP[self.op]}(self.left)")

    def repr(self):
        return self.visit().repr()


class IfNode(SpecialExpression):
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


class Assignment(SpecialExpression):
    """Assignment manager for the language."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def visit(self):
        ENV[self.name] = self.value
        return self.value


class Function(BaseObject):
    """Base function class for the language."""

    def repr(self):
        return f"<function {self.__class__.__name__}>"


class BuiltInFunction(Function):
    """Base class for built-in functions."""

    def repr(self):
        return f"<built-in function {self.__class__.__name__}>"

    def apply(self, args):
        for idx, arg in enumerate(args):
            setattr(self, f"arg{idx}", arg)


class Print(BuiltInFunction):
    """Print function."""

    def visit(self):
        return self

    def call(self, arg):
        print(result := arg.visit().repr())
        return result


class Input(BuiltInFunction):
    """Input function."""

    def visit(self):
        return String(input(self.arg0.visit().repr()))


class RandInt(BuiltInFunction):
    """Random integer function."""

    def visit(self):
        return Number(randint(1, self.arg0.visit().value))


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
        super().__setitem__(key, value)

    def __getitem__(self, key):
        return super().__getitem__(key)


ENV = Env(
    **{
        # Built-in functions
        "CONST_print": Print(),
        "CONST_input": Input(),
        "CONST_rand": RandInt(),
        # Special constants
        "CONST_true": Boolean(True),
        "CONST_false": Boolean(False),
        "CONST_null": Null(),
    }
)
