import pytest

from src.calculator import Calculator
from src.logger import Logger


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()

@pytest.fixture
def logger() -> Logger:
    return Logger()

def test_calculator_logger_addition(
    calculator: Calculator, logger: Logger, capsys: pytest.CaptureFixture[str],
) -> None:
    """Test Calculator operations with Logger."""
    result: float = calculator.add(5, 3)
    logger.log(f"Adding 5 + 3 = {result}")

    captured = capsys.readouterr()
    assert result == 8
    assert "LOG: Adding 5 + 3 = 8" in captured.out

def test_calculator_logger_subtraction(
    calculator: Calculator, logger: Logger, capsys: pytest.CaptureFixture[str],
) -> None:
    result: float = calculator.subtract(10, 4)
    logger.log(f"Subtracting 10 - 4 = {result}")

    captured = capsys.readouterr()
    assert result == 6
    assert "LOG: Subtracting 10 - 4 = 6" in captured.out

def test_calculator_logger_multiplication(
    calculator: Calculator, logger: Logger, capsys: pytest.CaptureFixture[str],
) -> None:
    result: float = calculator.multiply(6, 7)
    logger.log(f"Multiplying 6 * 7 = {result}")

    captured = capsys.readouterr()
    assert result == 42
    assert "LOG: Multiplying 6 * 7 = 42" in captured.out

def test_calculator_logger_division(
    calculator: Calculator, logger: Logger, capsys: pytest.CaptureFixture[str],
) -> None:
    result: float = calculator.divide(10, 2)
    logger.log(f"Dividing 10 / 2 = {result}")

    captured = capsys.readouterr()
    assert result == 5
    assert "LOG: Dividing 10 / 2 = 5.0" in captured.out

def test_calculator_logger_divide_by_zero(
    calculator: Calculator, logger: Logger, capsys: pytest.CaptureFixture[str],
) -> None:
    """Ensure dividing by zero raises an error and is logged."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(10, 0)
    logger.log("Attempted to divide by zero")

    captured = capsys.readouterr()
    assert "LOG: Attempted to divide by zero" in captured.out
