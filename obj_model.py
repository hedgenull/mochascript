from common import *

OP_TO_FUNC_MAP = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "%": "mod",
}


class BaseObject:
    pass


class Number(BaseObject):
    def __init__(self, value):
        self.value = int(value)

    def add(self, other):
        if isinstance(other, Number):
            return self.value + other.value
        elif isinstance(other, BinOp):
            return self.value + other.visit()
        else:
            abort(f"Invalid types for operation: Number and {type(other)}")

    def sub(self, other):
        if isinstance(other, Number):
            return self.value - other.value
        elif isinstance(other, BinOp):
            return self.value - other.visit()
        else:
            abort(f"Invalid types for operation: Number and {type(other)}")

    def mul(self, other):
        if isinstance(other, Number):
            return self.value * other.value
        elif isinstance(other, BinOp):
            return self.value * other.visit()
        else:
            abort(f"Invalid types for operation: Number and {type(other)}")

    def div(self, other):
        if isinstance(other, Number):
            return self.value / other.value
        elif isinstance(other, BinOp):
            return self.value / other.visit()
        else:
            abort(f"Invalid types for operation: Number and {type(other)}")

    def mod(self, other):
        if isinstance(other, Number):
            return self.value % other.value
        elif isinstance(other, BinOp):
            return self.value % other.visit()
        else:
            abort(f"Invalid types for operation: Number and {type(other)}")

    def visit(self):
        return self.value


class String(BaseObject):
    def __init__(self, value):
        self.value = value[1:-1]  # Strip leading and trailing quotes

    def add(self, other):
        if isinstance(other, String):
            return self.value + other.value
        else:
            abort(f"Invalid types for operation: String and {type(other)}")

    def mul(self, other):
        if isinstance(other, Number):
            return self.value * other.value
        else:
            abort(f"Invalid types for operation: String and {type(other)}")

    def mod(self, other):
        if isinstance(other, String):
            return self.value.replace("{}", other.value)
        else:
            abort(f"Invalid types for operation: String and {type(other)}")

    def visit(self):
        return self.value


class BinOp(BaseObject):
    def __init__(self, op, right, left):
        self.op = op
        self.right = right
        self.left = left

    def visit(self):
        return eval(f"self.right.{OP_TO_FUNC_MAP[self.op]}(self.left)")

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
