import unittest

from src.calculator.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_return(self) -> None:
        self.assertIsNotNone(self.calc.add(2, 3))
        self.assertIsNotNone(self.calc.subtract(6, 3))
        self.assertIsNotNone(self.calc.multiply(2, 3))
        self.assertIsNotNone(self.calc.divide(2, 3))

    def test_add(self)  -> None:
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self) -> None:
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self) -> None:
        self.assertEqual(self.calc.multiply(4, 2), 8)

    def test_divide(self) -> None:
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)

if __name__ == "__main__":
    unittest.main()
