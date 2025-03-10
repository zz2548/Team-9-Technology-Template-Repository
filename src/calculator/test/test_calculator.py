import unittest

from src.calculator.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Create a Calculator instance before each test."""
        self.calc = Calculator()

    def test_add(self):
        """Test addition"""
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        """Test subtraction"""
        self.assertEqual(self.calc.subtract(5, 3), 2)  # Missing test

    def test_multiply(self):
        """Test multiplication"""
        self.assertEqual(self.calc.multiply(4, 2), 8)  # Missing test

    def test_divide(self):
        """Test division"""
        self.assertEqual(self.calc.divide(10, 2), 5)  # Missing test

    def test_divide_by_zero(self):
        """Test division by zero, ensuring exception is raised"""
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)  # Missing test for zero division

if __name__ == "__main__":
    unittest.main()
