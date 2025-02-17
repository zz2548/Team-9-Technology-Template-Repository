from _pytest.capture import CaptureFixture

from src.notifier import Notifier


def test_notifier(capsys: CaptureFixture[str]) -> None:
    notifier = Notifier(10)
    notifier.notify(15)
    captured = capsys.readouterr()
    assert "ALERT: Value 15 exceeded threshold 10" in captured.out
