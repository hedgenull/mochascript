import unittest

from obj_model import *


class StringTestCase(unittest.TestCase):
    """Test cases for the String object."""
    def test_concatenation_with_string(self):
        string1 = String("A")
        string2 = String("B")
        expected = String("AB")

        self.assertEqual(string1.add(string2), expected, "String-string concatenation failed")

    def test_concatenation_with_other(self):
        string = String("123")
        array = Array([Number(1), Number(2), Number(3)])
        expected = String("123[1, 2, 3]")

        self.assertEqual(string.add(array), expected, "String-other concatenation failed")

    def test_subtraction(self):
        string1 = String("abcdef")
        string2 = String("abc")
        expected = String("def")

        self.assertEqual(string1.sub(string2), expected, "String subtraction failed")

    def test_multiplication(self):
        string = String("ko")
        three = Number(3)
        expected = String("kokoko")

        self.assertEqual(string.mul(three), expected, "String multiplication failed")

    def test_division(self):
        string = String("abcdef")
        zero = Number(0)
        expected = String("a")

        self.assertEqual(string.div(zero), expected, "String division failed")

    def test_format(self):
        hello = String("hello {}!")
        world = String("world")
        expected = String("hello world!")

        self.assertEqual(hello.mod(world), expected, "String formatting/modulus failed")


if __name__ == "__main__":
    unittest.main()
