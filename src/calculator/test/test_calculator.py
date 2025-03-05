import pytest

from src.calculator import Calculator, default_calculator, add, subtract, multiply, divide


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()


def test_add(calculator: Calculator) -> None:
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0, 0) == 0
    assert calculator.add(2.5, 3.5) == 6.0


def test_subtract(calculator: Calculator) -> None:
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(3, 5) == -2
    assert calculator.subtract(0, 0) == 0
    assert calculator.subtract(10.5, 5.5) == 5.0


def test_multiply(calculator: Calculator) -> None:
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(0, 5) == 0
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(2.5, 2) == 5.0


def test_divide(calculator: Calculator) -> None:
    assert calculator.divide(6, 3) == 2
    assert calculator.divide(5, 2) == 2.5
    assert calculator.divide(0, 5) == 0
    assert calculator.divide(-6, 2) == -3


def test_divide_by_zero(calculator: Calculator) -> None:
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(5, 0)


# API Tests
def test_calculator_api() -> None:
    # Test that the Calculator class is properly exposed


    # Test direct class usage
    calc = Calculator()
    assert calc.add(3, 4) == 7
    assert calc.subtract(10, 3) == 7

    # Test default instance
    assert default_calculator.multiply(4, 4) == 16

    # Test function exports
    assert add(7, 8) == 15
    assert subtract(25, 10) == 15
    assert multiply(5, 5) == 25
    assert divide(20, 4) == 5

    # Test error handling
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)