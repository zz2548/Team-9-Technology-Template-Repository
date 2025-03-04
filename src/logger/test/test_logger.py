from _pytest.capture import CaptureFixture

from logger import Logger


def test_logger(capsys: CaptureFixture[str]) -> None:
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert "LOG: Test message" in captured.out

