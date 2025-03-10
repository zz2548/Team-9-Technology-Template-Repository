import unittest


from src.calculator import (
    Calculator,
    add,
    default_calculator,
    divide,
    multiply,
    subtract,
)


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

    def test_calculator_api(self)-> None:
        # Test direct class usage
        calc = Calculator()
        self.assertEqual(calc.add(3, 4), 7)
        self.assertEqual(calc.subtract(10, 3), 7)

        # Test default instance
        self.assertEqual(default_calculator.multiply(4, 4), 16)

        # Test function exports
        self.assertEqual(add(7, 8), 15)
        self.assertEqual(subtract(25, 10), 15)
        self.assertEqual(multiply(5, 5), 25)
        self.assertEqual(divide(20, 4), 5)


if __name__ == "__main__":
    unittest.main()
