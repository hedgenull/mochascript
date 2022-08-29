import unittest

from obj_model import *


class ArrayTestCase(unittest.TestCase):
    """Tests for MochaScript's Array object."""

    def test_append(self):
        """Test Array appending (addition to another object)."""
        numbers = Array([Number(1), Number(2), Number(3), Number(4)])
        five = Number(5)
        expected = Array([Number(1), Number(2), Number(3), Number(4), Number(5)])

        self.assertEqual(numbers.add(five), expected, "Array appending failed")

    def test_remove(self):
        """Test Array removing (subtraction with another object)."""
        letters = Array([String("a"), String("b"), String("c")])
        letter_a = String("a")
        expected = Array([String("b"), String("c")])

        self.assertEqual(letters.sub(letter_a), expected, "Array removing failed")

    def test_multiplication(self):
        """Test Array multiplication."""
        numbers = Array([Number(1), Number(5), Number(7)])
        two = Number(2)
        expected = Array([Number(1), Number(5), Number(7), Number(1), Number(5), Number(7)])

        self.assertEqual(numbers.mul(two), expected, "Array multiplication failed")

    def test_indexing(self):
        """Test Array indexing (division with a Number)."""
        stuff = Array([String("shoes"), String("bag"), String("pencil")])
        first = Number(0)
        expected = String("shoes")

        self.assertEqual(stuff.div(first), expected, "Array indexing failed")
