import unittest

from src.calculator.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_add(self)  -> None:
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self) -> None:
        self.assertEqual(self.calc.subtract(5, 3), 2)  # Missing test

    def test_multiply(self) -> None:
        self.assertEqual(self.calc.multiply(4, 2), 8)  # Missing test

    def test_divide(self) -> None:
        self.assertEqual(self.calc.divide(10, 2), 5)  # Missing test

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)  # Missing test for zero division

if __name__ == "__main__":
    unittest.main()
