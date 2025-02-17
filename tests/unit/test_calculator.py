import pytest

from src.calculator import Calculator


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()

def test_add(calculator: Calculator) -> None:
    assert calculator.add(2, 3) == 5

def test_subtract(calculator: Calculator) -> None:
    assert calculator.subtract(5, 3) == 2

def test_multiply(calculator: Calculator) -> None:
    assert calculator.multiply(2, 3) == 6
