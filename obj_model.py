from utils import *

BINOP_TO_FUNC_MAP = {
    "+": "add",
    "-": "sub",
    "**": "exp",
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
    "in": "contains",
}

UNOP_TO_FUNC_MAP = {
    "+": "pos",
    "-": "neg",
}


class BaseObject:
    """Base class for all objects in MochaScript."""

    def add(self, other):
        return self.visit().add(other.visit())

    def sub(self, other):
        return self.visit().sub(other.visit())

    def exp(self, other):
        return self.visit().exp(other.visit())

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
        return Boolean(self.visit() == other.visit())

    def ne(self, other):
        return Boolean(self.visit().value != other.visit().value)

    def pos(self):
        return +self.value

    def neg(self):
        return -self.value

    def _and(self, other):
        return Boolean(
            Boolean(self.visit().value).value and Boolean(other.visit().value).value
        )

    def _or(self, other):
        return Boolean(
            Boolean(self.visit().value).value or Boolean(other.visit().value).value
        )

    def visit(self):
        return self

    def str(self):
        return str(self.value)

    def repr(self):
        return str(self.value)

    def type(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__ + str(
            {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and type(self) == type(other)


class Atom(BaseObject):
    """Base class for all atoms- i.e. objects that have a "value" attribute"""


class Number(Atom):
    """Number class for MochaScript."""

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

    def exp(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value)
        elif isinstance(other, SpecialExpression):
            return self.exp(other.visit())
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
        return Number(abs(self.value))

    def neg(self):
        return Number(-self.value)

    def repr(self):
        return (
            (str(self.value)[:-2] if self.value % 1 == 0 else str(self.value))
            if self.value
            else "0"
        )

    str = repr


class Array(Atom):
    """Array/list class for MochaScript."""

    def __init__(self, values=None):
        if values is None:
            values = []
        self.value = [value.visit() for value in values]

    def add(self, other):
        if isinstance(other, Array):
            return Array(self.value.extend(other.value))
        elif isinstance(other, Atom):
            return Array(self.value + [other.visit()])
        elif isinstance(other, SpecialExpression):
            return self.add(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def sub(self, other):
        if isinstance(other, Atom):
            copy = self.value[:]
            copy.remove(other)
            return Array(copy)
        elif isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def mul(self, other):
        if isinstance(other, Number):
            return Array(self.value * int(other.value))
        elif isinstance(other, SpecialExpression):
            return self.mul(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def div(self, other):
        if isinstance(other, Number):
            return self.value[int(other.value)]
        elif isinstance(other, SpecialExpression):
            return self.div(other.visit())
        abort(f"Invalid types for operation: Array and {type(other).__name__}")

    def contains(self, other):
        return Boolean(vars(other) in [vars(item) for item in self.value])

    def neg(self):
        return Array(self.value[::-1])

    def repr(self):
        return f"[{', '.join((value.repr() for value in self.value))}]"


class String(Array):
    """String class for MochaScript."""

    def __init__(self, value=""):
        self.value = (
            value.strip('"')
            .replace(r"\n", "\n")
            .replace(r"\t", "\t")
            .replace(r"\\", "\\")
        )

    def add(self, other):
        if isinstance(other, SpecialExpression):
            return self.add(other.visit())
        return String(self.value + other.str())

    def sub(self, other):
        if isinstance(other, SpecialExpression):
            return self.sub(other.visit())
        return String(self.value.replace(other.str(), ""))

    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * int(other.value))
        elif isinstance(other, SpecialExpression):
            return self.mul(int(other.visit()))
        abort(f"Invalid types for operation: String and {type(other).__name__}")

    def div(self, other):
        if isinstance(other, Number):
            return String(self.value[int(other.value)])
        elif isinstance(other, SpecialExpression):
            return self.div(other.visit())
        abort(f"Invalid types for operation: String and {type(other).__name__}")

    def mod(self, other):
        if isinstance(other, SpecialExpression):
            return self.mod(other.visit())
        return String(self.value.replace("{}", other.str()))

    def lt(self, other):
        return Boolean(len(self.visit().value) < len(other.visit().value))

    def gt(self, other):
        return Boolean(len(self.visit().value) > len(other.visit().value))

    def le(self, other):
        return Boolean(len(self.visit().value) <= len(other.visit().value))

    def ge(self, other):
        return Boolean(len(self.visit().value) >= len(other.visit().value))

    def pos(self):
        return String(self.value.upper())

    def neg(self):
        return String(self.value.lower())

    def repr(self):
        return f'"{self.value}"'


class Boolean(Atom):
    """Boolean class for MochaScript."""

    def __init__(self, value=True):
        self.value = bool(value)

    def repr(self):
        return str(self.value).lower()


class Function(Atom):
    """Function class for MochaScript."""

    def __init__(self, body, parameters, closure_env=None, name=None):
        self.body = body
        self.parameters = parameters
        self.closure_env = closure_env or {}
        self.name = name
        self.value = self.repr()

    def repr(self):
        return f"<function {self.name}>" if self.name else "<anonymous function object>"

    def call(self, arguments):
        """Call the function with arguments"""
        # Append the passed arguments to the environment
        _assignments = [
            k.visit() for k in arguments.keys() if isinstance(k, AssignmentNode)
        ]
        arguments = {
            k: v for k, v in arguments.items() if not isinstance(k, AssignmentNode)
        }
        updated_args = {**ENV[-1], **self.closure_env, **arguments}
        ENV.append(MSEnv(**updated_args))
        # Get the result of the function
        result = self.body.visit()
        if isinstance(result, Function):
            result.closure_env = ENV[-1]
        # Remove the arguments from the environment
        ENV.pop()
        return result

    add = lambda self, other: abort(
        f"Invalid types for operation: Function and {type(other).__name__}"
    )
    sub = add
    mul = add
    div = add
    mod = add
    _or = add
    _and = add
    le = add
    ge = add
    lt = add
    gt = add
    eq = add
    ne = add

    pos = lambda self: abort(f"Invalid type for operation: Function")
    neg = pos


class SpecialExpression(BaseObject):
    """Special expression base class for MochaScript."""


class BinOp(SpecialExpression):
    """Binary operation class for MochaScript."""

    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def visit(self):
        return eval(f"self.right.{BINOP_TO_FUNC_MAP[self.op]}(self.left)")

    def repr(self):
        return self.visit().repr()


class UnOp(SpecialExpression):
    """Unary operation class for MochaScript."""

    def __init__(self, op, value):
        self.op = op
        self.value = value

    def visit(self):
        return eval(f"self.value.{UNOP_TO_FUNC_MAP[self.op]}()")


class IfNode(SpecialExpression):
    """If-expression class for MochaScript."""

    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def visit(self):
        return (
            self.true_block.visit()
            if self.condition.visit().value
            else self.false_block.visit()
        )


class WhileNode(SpecialExpression):
    """While loop class for MochaScript."""

    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def visit(self):
        result = None

        while self.condition.visit().value:
            result = self.block.visit()
        return result


class ForNode(SpecialExpression):
    """For-loop class for MochaScript."""

    def __init__(self, iterator, var, body):
        self.iterator = iterator
        self.var = var
        self.body = body

    def visit(self):
        # Reduce the iterator to a single atom
        self.iterator = self.iterator.visit()

        # Ensure that the iterator is an actual iterator
        if not isinstance(self.iterator, Array):
            abort("For-loop can only accept an iterator")

        # Get the start and end of the array
        self.start, self.end = 0, len(self.iterator.value)

        # Set result and initialize new environment
        result = None
        ENV.append(MSEnv(**ENV[-1]))
        ENV[-1][self.var] = Boolean(False)

        # Iterate over the array
        while self.start != self.end:
            ENV[-1][self.var] = self.iterator.value[self.start]
            result = self.body.visit()
            self.start += 1

        return result


class RangeNode(SpecialExpression):
    """Range class for MochaScript."""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def visit(self):
        return Array(
            [
                Number(n)
                for n in range(
                    int(self.start.visit().value), int(self.end.visit().value + 1)
                )
            ]
        )


class SayNode(SpecialExpression):
    """It says the expression."""

    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        result = self.expr.visit()
        print(result.str())
        return result


class AskNode(SpecialExpression):
    """Get user input."""

    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return String(input(self.expr.visit().str()))


class ExitNode(SpecialExpression):
    """It says the expression, and then exits."""

    def __init__(self, expr=String()):
        self.expr = expr

    def visit(self):
        abort(self.expr.visit().str())


class BlockNode(SpecialExpression):
    """Multiple lines of code."""

    def __init__(self, *exprs):
        self.exprs = exprs

    def visit(self):
        return [expr.visit() for expr in self.exprs][-1]


class CallFunctionNode(SpecialExpression):
    """Calls a function."""

    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

    def visit(self):
        self.function = self.function.visit()
        if hasattr(self.function, "call"):
            self.arguments = {
                key: val.visit()
                for key, val in dict(
                    zip(self.function.parameters, self.arguments)
                ).items()
            }
            result = self.function.call(self.arguments)
        else:
            abort(f"{self.function.repr()} is not a callable object!")
        return result


class AssignmentNode(SpecialExpression):
    """Assignment manager for MochaScript."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def visit(self):
        ENV[-1][self.name] = self.value.visit()
        return ENV[-1][self.name]


class InPlaceAssignmentNode(SpecialExpression):
    """In-place assignment manager for MochaScript."""

    def __init__(self, op, name, value):
        self.op = op
        self.name = name
        self.value = value

    def visit(self):
        return AssignmentNode(
            self.name, BinOp(self.op, ReferenceNode(self.name), self.value)
        ).visit()


class ReferenceNode(SpecialExpression):
    """Reference manager for MochaScript."""

    def __init__(self, name):
        self.name = name

    def visit(self):
        value = ENV[-1].get(self.name)
        if not value:
            abort(f"Undefined variable {self.name}")
        return value


class MSEnv(dict):
    pass


ENV = [MSEnv()]
