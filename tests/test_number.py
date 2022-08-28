import unittest

from obj_model import *


class NumberTestCase(unittest.TestCase):
    def test_addition(self):
        one = Number(1)
        three = Number(3)
        four = Number(4)

        self.assertEqual(one.add(three), four, "Addition failed")

    def test_subtraction(self):
        five = Number(5)
        two = Number(2)
        three = Number(3)

        self.assertEqual(five.sub(two), three, "Subtraction failed")

    def test_multiplication(self):
        four = Number(4)
        three = Number(3)
        twelve = Number(12)

        self.assertEqual(four.mul(three), twelve, "Multiplication failed")

    def test_division(self):
        five = Number(5)
        two = Number(2)
        two_point_five = Number(2.5)

        self.assertAlmostEqual(five.div(two), two_point_five, "Division failed")

    def test_modulo(self):
        five = Number(5)
        two = Number(2)
        one = Number(1)

        self.assertAlmostEqual(five.mod(two), one, "Modulo failed")

    def test_positive(self):
        negative_two = Number(-2)
        two = Number(2)

        self.assertEqual(
            negative_two.pos(), two, "Positive of a negative number should be positive"
        )

    def test_negative(self):
        negative_two = Number(-2)
        two = Number(2)

        self.assertEqual(two.neg(), negative_two, "Negation failed")


if __name__ == "__main__":
    unittest.main()
