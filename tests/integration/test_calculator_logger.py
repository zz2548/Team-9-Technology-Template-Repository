import unittest
import io
from unittest.mock import patch

from src.calculator.calculator import Calculator
from src.logger.logger import Logger


class TestCalculatorLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()
        self.logger = Logger()

    def test_calculator_logger_addition(self) -> None:
        """Test Calculator operations with Logger."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result: float = self.calculator.add(5, 3)
            self.logger.log(f"Adding 5 + 3 = {result}")

            captured_output = mock_stdout.getvalue()
            assert result == 8, f"Expected 8, got {result}"
            assert "LOG: Adding 5 + 3 = 8" in captured_output, "Incorrect log output"

    def test_calculator_logger_subtraction(self) -> None:
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result: float = self.calculator.subtract(10, 4)
            self.logger.log(f"Subtracting 10 - 4 = {result}")

            captured_output = mock_stdout.getvalue()
            assert result == 6, f"Expected 6, got {result}"
            assert "LOG: Subtracting 10 - 4 = 6" in captured_output, "Incorrect log output"

    def test_calculator_logger_multiplication(self) -> None:
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result: float = self.calculator.multiply(6, 7)
            self.logger.log(f"Multiplying 6 * 7 = {result}")

            captured_output = mock_stdout.getvalue()
            assert result == 42, f"Expected 42, got {result}"
            assert "LOG: Multiplying 6 * 7 = 42" in captured_output, "Incorrect log output"

    def test_calculator_logger_division(self) -> None:
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result: float = self.calculator.divide(10, 2)
            self.logger.log(f"Dividing 10 / 2 = {result}")

            captured_output = mock_stdout.getvalue()
            assert result == 5, f"Expected 5, got {result}"
            assert "LOG: Dividing 10 / 2 = 5.0" in captured_output, "Incorrect log output"

    def test_calculator_logger_divide_by_zero(self) -> None:
        """Ensure dividing by zero raises an error and is logged."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ValueError, msg="Cannot divide by zero"):
                self.calculator.divide(10, 0)
            self.logger.log("Attempted to divide by zero")

            captured_output = mock_stdout.getvalue()
            assert "LOG: Attempted to divide by zero" in captured_output, "Incorrect log output"


if __name__ == "__main__":
    unittest.main()