import unittest

from src.calculator import Calculator, default_calculator, add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    def setUp(self)-> None:
        self.calculator = Calculator()

    def test_add(self)-> None:
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-1, 1), 0)
        self.assertEqual(self.calculator.add(0, 0), 0)
        self.assertEqual(self.calculator.add(2.5, 3.5), 6.0)

    def test_subtract(self)-> None:
        self.assertEqual(self.calculator.subtract(5, 3), 2)
        self.assertEqual(self.calculator.subtract(3, 5), -2)
        self.assertEqual(self.calculator.subtract(0, 0), 0)
        self.assertEqual(self.calculator.subtract(10.5, 5.5), 5.0)

    def test_multiply(self)-> None:
        self.assertEqual(self.calculator.multiply(2, 3), 6)
        self.assertEqual(self.calculator.multiply(0, 5), 0)
        self.assertEqual(self.calculator.multiply(-2, 3), -6)
        self.assertEqual(self.calculator.multiply(2.5, 2), 5.0)

    def test_divide(self)-> None:
        self.assertEqual(self.calculator.divide(6, 3), 2)
        self.assertEqual(self.calculator.divide(5, 2), 2.5)
        self.assertEqual(self.calculator.divide(0, 5), 0)
        self.assertEqual(self.calculator.divide(-6, 2), -3)

    def test_divide_by_zero(self)-> None:
        with self.assertRaises(ValueError) as context:
            self.calculator.divide(5, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")

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

        # Test error handling
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")

if __name__ == "__main__":
    unittest.main()