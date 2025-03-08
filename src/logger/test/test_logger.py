import io
import unittest
from unittest.mock import patch

from src.logger import Logger, default_logger, log


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = Logger()

    def test_logger(self) -> None:
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.logger.log("Test message")
            captured_output = mock_stdout.getvalue()
            self.assertIn("LOG: Test message", captured_output)

    def test_logger_api(self) -> None:
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test direct class usage
            custom_logger = Logger()
            custom_logger.log("Custom logger test")
            captured_output = mock_stdout.getvalue()
            self.assertIn("LOG: Custom logger test", captured_output)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test default instance
            default_logger.log("Default logger test")
            captured_output = mock_stdout.getvalue()
            self.assertIn("LOG: Default logger test", captured_output)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test direct function usage
            log("Direct log function")
            captured_output = mock_stdout.getvalue()
            self.assertIn("LOG: Direct log function", captured_output)


if __name__ == "__main__":
    unittest.main()
