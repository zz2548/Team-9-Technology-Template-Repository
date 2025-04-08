import io
from unittest.mock import patch

import pytest

from src.logger import Logger, default_logger, log


class TestLogger:
    @pytest.fixture
    def logger(self) -> Logger:
        return Logger()

    def test_logger(self, logger: Logger) -> None:
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            logger.log("Test message")
            captured_output = mock_stdout.getvalue()
            assert "LOG: Test message" in captured_output

    def test_logger_api(self) -> None:
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test direct class usage
            custom_logger = Logger()
            custom_logger.log("Custom logger test")
            captured_output = mock_stdout.getvalue()
            assert "LOG: Custom logger test" in captured_output

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test default instance
            default_logger.log("Default logger test")
            captured_output = mock_stdout.getvalue()
            assert "LOG: Default logger test" in captured_output

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test direct function usage
            log("Direct log function")
            captured_output = mock_stdout.getvalue()
            assert "LOG: Direct log function" in captured_output


if __name__ == "__main__":
    pytest.main()
