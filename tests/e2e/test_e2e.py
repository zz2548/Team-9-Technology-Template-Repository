import pytest


from src.calculator.calculator import Calculator
from src.logger.logger import Logger
from src.notifier.notifier import Notifier


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
    """Test the full end-to-end flow."""
    # Step 1: Perform a calculation using the Calculator
    result: float = calculator.add(5, 10)

    # Step 2: Log the result using the Logger
    logger.log(f"Result of 5 + 10 = {result}")

    # Step 3: Notify if the result exceeds the threshold using the Notifier
    notifier.notify(result)

    # Capture the output
    captured = capsys.readouterr()

    # Assertions for calculation and logging
    assert result == 15
    assert "LOG: Result of 5 + 10 = 15" in captured.out

    # Assertions for the notifier (should trigger since threshold is 10)
    assert (
        "ALERT: Value 15 exceeded threshold 10"
        in captured.out
    )
