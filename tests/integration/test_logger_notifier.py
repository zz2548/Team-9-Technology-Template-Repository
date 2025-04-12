import io
from unittest.mock import patch

import pytest

import logger
import notifier


@pytest.fixture
def log():
    return logger.Logger()


@pytest.fixture
def notify():
    return notifier.Notifier(threshold=10)


def test_logger_notifier_no_alert(log, notify) -> None:
    """
    Test that the notifier does not send an alert when a value is below the threshold.

    This test verifies:
    1. The logger correctly logs the operation message
    2. The notifier correctly evaluates the value against its threshold
    3. No alert is generated when the value (5) is below the threshold (10)
    4. Only the expected log message appears in the output
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        log.log("Performing a safe operation")
        notify.notify(5)  # Below threshold, should not trigger

        captured_output = mock_stdout.getvalue()
        assert "LOG: Performing a safe operation" in captured_output
        assert "ALERT" not in captured_output, "Unexpected alert triggered"


def test_logger_notifier_with_alert(log, notify) -> None:
    """
    Test that the notifier sends an alert when a value exceeds the threshold.

    This test verifies:
    1. The logger correctly logs the operation message
    2. The notifier correctly evaluates the value against its threshold
    3. An alert is generated when the value (15) exceeds the threshold (10)
    4. Both the log message and alert message appear in the output
    5. The alert message contains the correct value and threshold information
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        log.log("Checking if value exceeds threshold")
        notify.notify(15)  # Exceeds threshold

        captured_output = mock_stdout.getvalue()
        assert "LOG: Checking if value exceeds threshold" in captured_output
        assert "ALERT: Value 15 exceeded threshold 10" in captured_output


if __name__ == "__main__":
    pytest.main()
