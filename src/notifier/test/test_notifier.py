import io
import unittest
from unittest.mock import patch

from src.notifier import Notifier, __authors__, __version__


class TestNotifier(unittest.TestCase):
    def test_notifier(self) -> None:
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            notifier = Notifier(10)
            notifier.notify(15)
            captured_output = mock_stdout.getvalue()
            self.assertIn("ALERT: Value 15 exceeded threshold 10", captured_output)

    def test_notifier_metadata(self) -> None:
        # Test version
        self.assertEqual(__version__, "0.1.0")

        # Test authors list
        self.assertEqual(len(__authors__), 4)
        self.assertEqual(__authors__[0]["name"], "Jerry Zou")
        self.assertEqual(__authors__[1]["name"], "Keshav Rajput")
        self.assertEqual(__authors__[2]["name"], "Terry Xu")
        self.assertEqual(__authors__[3]["name"], "Jinglin Tao")


if __name__ == "__main__":
    unittest.main()
