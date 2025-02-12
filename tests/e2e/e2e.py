import pytest
from src.calculator import Calculator
from src.logger import Logger
from src.notifier import Notifier

# Fixtures for the components
@pytest.fixture
def calculator() -> Calculator:
    return Calculator()

@pytest.fixture
def logger() -> Logger:
    return Logger()

@pytest.fixture
def notifier() -> Notifier:
    return Notifier(threshold=10)

def test_end_to_end_flow(
    calculator: Calculator,
    logger: Logger,
    notifier: Notifier,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test the full end-to-end flow"""
    
    result: float = calculator.add(5, 10)
    
    logger.log(f"Result of 5 + 10 = {result}")

    notifier.notify(result)

    captured = capsys.readouterr()

    assert result == 15
    assert "LOG: Result of 5 + 10 = 15" in captured.out

    assert (
        "ALERT: Value 15 exceeded threshold 10"
        in captured.out
    )
