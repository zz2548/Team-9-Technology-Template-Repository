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

            # Step 3: Notify if the result exceeds the threshold using the Notifier
            self.notifier.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions for calculation and logging
            self.assertEqual(result, 15)
            self.assertIn("LOG: Result of 5 + 10 = 15", captured_output)

            # Assertions for the notifier (should trigger since threshold is 10)
            self.assertIn("ALERT: Value 15 exceeded threshold 10", captured_output)

if __name__ == "__main__":
    unittest.main()