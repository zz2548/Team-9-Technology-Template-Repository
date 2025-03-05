from _pytest.capture import CaptureFixture

from src.logger import Logger, default_logger, log


def test_logger(capsys: CaptureFixture[str]) -> None:
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert "LOG: Test message" in captured.out


def test_logger_api(capsys):
    # Test direct class usage
    custom_logger = Logger()
    custom_logger.log("Custom logger test")
    captured = capsys.readouterr()
    assert "LOG: Custom logger test" in captured.out

    # Test default instance
    default_logger.log("Default logger test")
    captured = capsys.readouterr()
    assert "LOG: Default logger test" in captured.out

    # Test direct function usage
    log("Direct log function")
    captured = capsys.readouterr()
    assert "LOG: Direct log function" in captured.out