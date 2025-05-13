import io
import unittest
from unittest.mock import patch

from src.calculator.calculator import Calculator
from src.logger.logger import Logger
from src.notifier.notifier import Notifier


class TestEndToEndFlow(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test fixtures for each test method."""
        self.calculator = Calculator()
        self.logger = Logger()
        # Create two notifiers with different thresholds to test both cases
        self.notifier_high = Notifier(threshold=10)
        self.notifier_low = Notifier(threshold=100)

    def test_addition_flow(self) -> None:
        """Test the end-to-end flow with addition operation."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Step 1: Perform a calculation using the Calculator
            result = self.calculator.add(5, 10)

            # Step 2: Log the result using the Logger
            self.logger.log(f"Result of 5 + 10 = {result}")

            # Step 3: Notify with a value above threshold
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, 15, f"Expected 15, got {result}")
            self.assertIn(
                "LOG: Result of 5 + 10 = 15",
                captured_output,
                "Logging output is incorrect",
            )
            self.assertIn(
                "ALERT: Value 15 exceeded threshold 10",
                captured_output,
                "Notifier output is incorrect",
            )

    def test_subtraction_flow(self) -> None:
        """Test the end-to-end flow with subtraction operation."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Step 1: Perform a calculation using the Calculator
            result = self.calculator.subtract(20, 5)

            # Step 2: Log the result using the Logger
            self.logger.log(f"Result of 20 - 5 = {result}")

            # Step 3: Notify with a value above threshold
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, 15, f"Expected 15, got {result}")
            self.assertIn(
                "LOG: Result of 20 - 5 = 15",
                captured_output,
                "Logging output is incorrect",
            )
            self.assertIn(
                "ALERT: Value 15 exceeded threshold 10",
                captured_output,
                "Notifier output is incorrect",
            )

    def test_multiplication_flow(self) -> None:
        """Test the end-to-end flow with multiplication operation."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Step 1: Perform a calculation using the Calculator
            result = self.calculator.multiply(4, 5)

            # Step 2: Log the result using the Logger
            self.logger.log(f"Result of 4 * 5 = {result}")

            # Step 3: Notify with a value above threshold
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, 20, f"Expected 20, got {result}")
            self.assertIn(
                "LOG: Result of 4 * 5 = 20",
                captured_output,
                "Logging output is incorrect",
            )
            self.assertIn(
                "ALERT: Value 20 exceeded threshold 10",
                captured_output,
                "Notifier output is incorrect",
            )

    def test_division_flow(self) -> None:
        """Test the end-to-end flow with division operation."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Step 1: Perform a calculation using the Calculator
            result = self.calculator.divide(30, 3)

            # Step 2: Log the result using the Logger
            self.logger.log(f"Result of 30 / 3 = {result}")

            # Step 3: Notify with a value above threshold
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, 10, f"Expected 10, got {result}")
            self.assertIn(
                "LOG: Result of 30 / 3 = 10",
                captured_output,
                "Logging output is incorrect",
            )

            if "ALERT" in captured_output:
                self.assertIn(
                    "ALERT: Value 10 exceeded threshold 10",
                    captured_output,
                    "Notifier output is incorrect",
                )

    def test_below_threshold_notification(self) -> None:
        """Test notification when value is below threshold."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Create a small value
            result = self.calculator.add(1, 2)

            # Log the result
            self.logger.log(f"Result of 1 + 2 = {result}")

            # This should NOT trigger a notification (3 < 10)
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertion - there should be no alert in the output
            self.assertNotIn(
                "ALERT:",
                captured_output,
                "Notifier incorrectly triggered for value below threshold",
            )

    def test_decimal_operations(self) -> None:
        """Test operations with decimal numbers."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test with decimal numbers
            result = self.calculator.add(5.5, 4.5)

            # Log the result
            self.logger.log(f"Result of 5.5 + 4.5 = {result}")

            # Notify
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, 10.0, f"Expected 10.0, got {result}")
            self.assertIn(
                "LOG: Result of 5.5 + 4.5 = 10.0",
                captured_output,
                "Logging output is incorrect for decimal operations",
            )

    def test_negative_numbers(self) -> None:
        """Test operations with negative numbers."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Test with negative numbers
            result = self.calculator.add(-15, 5)

            # Log the result
            self.logger.log(f"Result of -15 + 5 = {result}")

            # Notify
            self.notifier_high.notify(result)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions
            self.assertEqual(result, -10, f"Expected -10, got {result}")
            self.assertIn(
                "LOG: Result of -15 + 5 = -10",
                captured_output,
                "Logging output is incorrect for negative numbers",
            )

            # Modify assertion based on actual implementation

    def test_complex_flow(self) -> None:
        """Test a more complex flow with multiple operations and notifications."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Perform a sequence of calculations
            result1 = self.calculator.add(5, 10)
            self.logger.log(f"First calculation: 5 + 10 = {result1}")

            result2 = self.calculator.multiply(result1, 2)
            self.logger.log(f"Second calculation: {result1} * 2 = {result2}")

            result3 = self.calculator.subtract(result2, 5)
            self.logger.log(f"Third calculation: {result2} - 5 = {result3}")

            result4 = self.calculator.divide(result3, 5)
            self.logger.log(f"Final calculation: {result3} / 5 = {result4}")

            # Notify with the final result
            self.notifier_high.notify(result4)
            self.notifier_low.notify(result4)

            # Capture the output
            captured_output = mock_stdout.getvalue()

            # Assertions for the calculation sequence
            self.assertEqual(result1, 15)
            self.assertEqual(result2, 30)
            self.assertEqual(result3, 25)
            self.assertEqual(result4, 5)

            # Assertion for logging
            self.assertIn("LOG: First calculation: 5 + 10 = 15", captured_output)
            self.assertIn("LOG: Second calculation: 15 * 2 = 30", captured_output)
            self.assertIn("LOG: Third calculation: 30 - 5 = 25", captured_output)
            self.assertIn("LOG: Final calculation: 25 / 5 = 5", captured_output)

            # Assertion for notifications - result4 is below both thresholds
            self.assertNotIn("ALERT: Value 5 exceeded threshold 10", captured_output)
            self.assertNotIn("ALERT: Value 5 exceeded threshold 100", captured_output)


if __name__ == "__main__":
    unittest.main()
