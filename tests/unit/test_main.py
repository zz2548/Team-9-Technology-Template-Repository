from src.main import main
import pytest

def test_main_execution(capfd: pytest.CaptureFixture[str]) -> None:
    main()
    out, err = capfd.readouterr()
    assert out.strip() == "3"
