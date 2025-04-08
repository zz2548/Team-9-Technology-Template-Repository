import io
from unittest.mock import patch

import pytest

import calculator
import logger


@pytest.fixture
def calc():
    return calculator.Calculator()


@pytest.fixture
def log():
    return logger.Logger()


def test_calculator_logger_addition(calc, log) -> None:
    """
    Test integration between Calculator and Logger for addition operations.

    Verifies that:
    1. Calculator correctly adds two numbers
    2. Logger properly logs the calculation result
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = calc.add(5, 3)
        log.log(f"Adding 5 + 3 = {result}")
        captured_output = mock_stdout.getvalue()
        assert result == 8, f"Expected 8, got {result}"
        assert "LOG: Adding 5 + 3 = 8" in captured_output, "Incorrect log output"


def test_calculator_logger_subtraction(calc, log) -> None:
    """
    Test integration between Calculator and Logger for subtraction operations.

    Verifies that:
    1. Calculator correctly subtracts one number from another
    2. Logger properly logs the calculation result
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = calc.subtract(10, 4)
        log.log(f"Subtracting 10 - 4 = {result}")
        captured_output = mock_stdout.getvalue()
        assert result == 6, f"Expected 6, got {result}"
        assert "LOG: Subtracting 10 - 4 = 6" in captured_output, "Incorrect log output"


def test_calculator_logger_multiplication(calc, log) -> None:
    """
    Test integration between Calculator and Logger for multiplication operations.

    Verifies that:
    1. Calculator correctly multiplies two numbers
    2. Logger properly logs the calculation result
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = calc.multiply(6, 7)
        log.log(f"Multiplying 6 * 7 = {result}")
        captured_output = mock_stdout.getvalue()
        assert result == 42, f"Expected 42, got {result}"
        assert "LOG: Multiplying 6 * 7 = 42" in captured_output, "Incorrect log output"


def test_calculator_logger_division(calc, log) -> None:
    """
    Test integration between Calculator and Logger for division operations.

    Verifies that:
    1. Calculator correctly divides one number by another
    2. Logger properly logs the calculation result
    3. Floating point results are handled correctly
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = calc.divide(10, 2)
        log.log(f"Dividing 10 / 2 = {result}")
        captured_output = mock_stdout.getvalue()
        assert result == 5, f"Expected 5, got {result}"
        assert "LOG: Dividing 10 / 2 = 5.0" in captured_output, "Incorrect log output"


def test_calculator_logger_divide_by_zero(calc, log) -> None:
    """
    Test error handling when dividing by zero.

    Verifies that:
    1. Calculator raises the correct exception when dividing by zero
    2. The exception contains the expected error message
    3. Logger can log information about the error
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        # Attempt to divide by zero and verify exception
        with pytest.raises(ValueError) as excinfo:
            calc.divide(10, 0)
        assert str(excinfo.value) == "Cannot divide by zero"

        # Log information about the error
        log.log("Attempted to divide by zero")
        # Capture and verify the logged output
        captured_output = mock_stdout.getvalue()
        assert "LOG: Attempted to divide by zero" in captured_output, (
            "Incorrect log output"
        )
