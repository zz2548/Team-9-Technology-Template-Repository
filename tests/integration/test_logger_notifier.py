import io
import unittest
from unittest.mock import patch

from src.logger.logger import Logger
from src.notifier.notifier import Notifier


class TestLoggerNotifier(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = Logger()
        self.notifier = Notifier(threshold=10)

    def test_logger_notifier_no_alert(self) -> None:
        """Test that notifier does not send an alert if value is below the threshold."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.logger.log("Performing a safe operation")
            self.notifier.notify(5)  # Below threshold, should not trigger

            captured_output = mock_stdout.getvalue()
            assert "LOG: Performing a safe operation" in captured_output
            assert "ALERT" not in captured_output, "Unexpected alert triggered"

    def test_logger_notifier_with_alert(self) -> None:
        """Test that notifier sends an alert when value exceeds the threshold."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.logger.log("Checking if value exceeds threshold")
            self.notifier.notify(15)  # Exceeds threshold

            captured_output = mock_stdout.getvalue()
            assert "LOG: Checking if value exceeds threshold" in captured_output
            assert "ALERT: Value 15 exceeded threshold 10" in captured_output


if __name__ == "__main__":
    unittest.main()
