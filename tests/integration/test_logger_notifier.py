import pytest

from src.logger.logger import Logger
from src.notifier.notifier import Notifier


@pytest.fixture
def logger() -> Logger:
    return Logger()

@pytest.fixture
def notifier() -> Notifier:
    return Notifier(threshold=10)

def test_logger_notifier_no_alert(
    logger: Logger, notifier: Notifier, capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that notifier does not send an alert if value is below the threshold."""
    logger.log("Performing a safe operation")
    notifier.notify(5)  # Below threshold, should not trigger

    captured = capsys.readouterr()
    assert "LOG: Performing a safe operation" in captured.out
    assert "ALERT" not in captured.out  # No alert expected

def test_logger_notifier_with_alert(
    logger: Logger, notifier: Notifier, capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that notifier sends an alert when value exceeds the threshold."""
    logger.log("Checking if value exceeds threshold")
    notifier.notify(15)  # Exceeds threshold

    captured = capsys.readouterr()
    assert "LOG: Checking if value exceeds threshold" in captured.out
    assert "ALERT: Value 15 exceeded threshold 10" in captured.out
