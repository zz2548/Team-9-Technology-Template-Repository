import unittest
import io
from unittest.mock import patch

from src.calculator.calculator import Calculator
from src.logger.logger import Logger
from src.notifier.notifier import Notifier


class TestEndToEndFlow(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()
        self.logger = Logger()
        self.notifier = Notifier(threshold=10)

    def test_end_to_end_flow(self) -> None:
        """Test the full end-to-end flow."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Step 1: Perform a calculation using the Calculator
            result = self.calculator.add(5, 10)

            # Step 2: Log the result using the Logger
            self.logger.log(f"Result of 5 + 10 = {result}")

            self.notifier.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions for calculation and logging using native assert
            assert result == 15, f"Expected 15, got {result}"
            assert ("LOG: Result of 5 + 10 = 15" in captured_output,
                    "Logging output is incorrect")

            # Assertions for the notifier (should trigger since threshold is 10)
            assert ("ALERT: Value 15 exceeded "
                    "threshold 10") in captured_output, "Notifier output is incorrect"

if __name__ == "__main__":
    unittest.main()