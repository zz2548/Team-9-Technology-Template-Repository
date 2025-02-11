from src.logger import Logger

def test_logger(capsys) -> None:
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert "LOG: Test message" in captured.out

