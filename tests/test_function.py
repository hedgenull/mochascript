import unittest

from obj_model import *


class FunctionTestCase(unittest.TestCase):
    """Test cases for the Function object."""

    def test_anonymous_func_name_repr(self):
        """Test anonymous function name and repr() method."""
        body = Number(5)  # The function just returns 5
        function = Function(body, [])  # Anonymous function- no name

        self.assertEqual(function.name, None, "Anonymous Function should not have a name")
        self.assertEqual(
            function.repr(), "<anonymous function object>", "Anonymous function repr() incorrect"
        )

    def test_named_func_name_repr(self):
        """Test named function name and repr() method."""
        body = Number(5)  # The function just returns 5
        function = Function(body, [], name="foo")  # Named function- name = "foo"

        self.assertEqual(function.name, "foo", "Named Function should have a name")
        self.assertEqual(function.repr(), "<function foo>", "Named Function repr() incorrect")

    def test_func_with_arguments(self):
        """Test function parameters."""
        body = BinOp("+", ReferenceNode("a"), ReferenceNode("b"))
        function = Function(
            body, ["a", "b"]
        )  # An anonymous function that adds two numbers together

        self.assertEqual(function.parameters, ["a", "b"], "Function parameters incorrect")

    def test_func_without_arguments(self):
        """Test empty function parameters."""
        body = String("Hello, world!")  # The function returns a string literal
        function = Function(body, [])

        self.assertEqual(function.parameters, [], "Empty function parameters incorrect")

    def test_func_with_arguments(self):
        """Test calling a function that accepts arguments."""
        body = BinOp("+", ReferenceNode("a"), ReferenceNode("b"))
        function = Function(
            body, ["a", "b"]
        )  # An anonymous function that adds two numbers together
        a = Number(5)  # First argument ("a")
        b = Number(2)  # Second argument ("b")
        callnode = CallFunctionNode(function, [a, b])  # Function caller object
        expected = a.add(b)  # Sum of 5 and 2

        self.assertEqual(callnode.visit(), expected, "Function call failed")  # Call the function

    def test_func_without_arguments(self):
        """Test calling a function with no arguments."""
        body = String("Hello, world!")  # The function returns a string literal
        function = Function(body, [])
        callnode = CallFunctionNode(function, [])  # Function caller object
        expected = String("Hello, world!")  # The expected return value

        self.assertEqual(callnode.visit(), expected, "Function call failed")  # Call the function


if __name__ == "__main__":
    unittest.main()
