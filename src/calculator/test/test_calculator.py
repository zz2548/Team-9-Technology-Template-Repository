import pytest

from src.calculator import (
    Calculator,
    add,
    default_calculator,
    divide,
    multiply,
    subtract,
)


class TestCalculator:
    @pytest.fixture
    def calc(self) -> Calculator:  # Changed return type from None to Calculator
        return Calculator()

    def test_return(self, calc: Calculator) -> None:
        assert calc.add(2, 3) is not None
        assert calc.subtract(6, 3) is not None
        assert calc.multiply(2, 3) is not None
        assert calc.divide(2, 3) is not None

    def test_add(self, calc: Calculator) -> None:
        assert calc.add(2, 3) == 5

    def test_subtract(self, calc: Calculator) -> None:
        assert calc.subtract(5, 3) == 2

    def test_multiply(self, calc: Calculator) -> None:
        assert calc.multiply(4, 2) == 8

    def test_divide(self, calc: Calculator) -> None:
        assert calc.divide(10, 2) == 5

    def test_divide_by_zero(self, calc: Calculator) -> None:
        with pytest.raises(ValueError):
            calc.divide(5, 0)

    def test_calculator_api(self) -> None:
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


if __name__ == "__main__":
    pytest.main()
