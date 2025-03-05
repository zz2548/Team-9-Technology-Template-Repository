from _pytest.capture import CaptureFixture

from src.notifier import Notifier


def test_notifier(capsys: CaptureFixture[str]) -> None:
    notifier = Notifier(10)
    notifier.notify(15)
    captured = capsys.readouterr()
    assert "ALERT: Value 15 exceeded threshold 10" in captured.out


def test_notifier_metadata():
    # Test that metadata is correctly exposed
    from src.notifier import __version__, __authors__

    # Test version
    assert __version__ == "0.1.0"

    # Test authors list
    assert len(__authors__) == 4
    assert __authors__[0]["name"] == "Jerry Zou"
    assert __authors__[1]["name"] == "Keshav Rajput"
    assert __authors__[2]["name"] == "Terry Xu"
    assert __authors__[3]["name"] == "Jinglin Tao"