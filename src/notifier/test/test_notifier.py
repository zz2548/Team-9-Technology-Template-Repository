import io
from unittest.mock import patch

import pytest

from src.notifier import Notifier


def test_notifier() -> None:
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        notifier = Notifier(10)
        notifier.notify(15)
        captured_output = mock_stdout.getvalue()
        assert "ALERT: Value 15 exceeded threshold 10" in captured_output


if __name__ == "__main__":
    pytest.main()
