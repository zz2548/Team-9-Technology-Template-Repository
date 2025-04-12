import io
from unittest.mock import patch

import pytest

import calculator
import logger
import notifier


@pytest.fixture
def calc():
    return calculator.Calculator()


@pytest.fixture
def log():
    return logger.Logger()


@pytest.fixture
def notifier_high():
    return notifier.Notifier(threshold=10)


@pytest.fixture
def notifier_low():
    return notifier.Notifier(threshold=100)


def execute_flow(log, notifier, operation, a, b, operation_name):
    """
    Execute a standardized calculation-logging-notification flow.

    This function encapsulates the common pattern used across multiple tests:
    1. Perform a calculation operation with two operands
    2. Log the result of the operation
    3. Send the result to the notifier for potential alerts
    4. Capture the console output and return it along with the calculation result
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = operation(a, b)
        log.log(f"Result of {a} {operation_name} {b} = {result}")
        notifier.notify(result)
        return mock_stdout.getvalue(), result


def test_addition_flow(calc, log, notifier_high) -> None:
    """
    Tests the complete flow of addition operations through the system.

    This test verifies that:
    1. The Calculator correctly adds two numbers (5 + 10)
    2. The Logger properly records the operation and result
    3. The Notifier correctly identifies the result (15) as exceeding
       the threshold (10) and generates an alert
    """
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.add,
        5,
        10,
        "+",
    )
    assert result == 15, f"Addition calculation failed: expected 15, got {result}"
    assert "LOG: Result of 5 + 10 = 15" in captured_output, (
        "Logger failed to record addition operation"
    )
    assert "ALERT: Value 15 exceeded threshold 10" in captured_output, (
        "Notifier failed to generate alert for above-threshold value"
    )


def test_subtraction_flow(calc, log, notifier_high) -> None:
    """
    Tests the complete flow of subtraction operations through the system.

    This test verifies that:
    1. The Calculator correctly subtracts one number from another (20 - 5)
    2. The Logger properly records the operation and result
    3. The Notifier correctly identifies the result (15) as exceeding
       the threshold (10) and generates an alert
    """
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.subtract,
        20,
        5,
        "-",
    )
    assert result == 15, f"Subtraction calculation failed: expected 15, got {result}"
    assert "LOG: Result of 20 - 5 = 15" in captured_output, (
        "Logger failed to record subtraction operation"
    )
    assert "ALERT: Value 15 exceeded threshold 10" in captured_output, (
        "Notifier failed to generate alert for above-threshold value"
    )


def test_multiplication_flow(calc, log, notifier_high) -> None:
    """
    Tests the complete flow of multiplication operations through the system.

    This test verifies that:
    1. The Calculator correctly multiplies two numbers (4 * 5)
    2. The Logger properly records the operation and result
    3. The Notifier correctly identifies the result (20) as exceeding
       the threshold (10) and generates an alert
    """
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.multiply,
        4,
        5,
        "*",
    )
    assert result == 20, f"Multiplication calculation failed: expected 20, got {result}"
    assert "LOG: Result of 4 * 5 = 20" in captured_output, (
        "Logger failed to record multiplication operation"
    )
    assert "ALERT: Value 20 exceeded threshold 10" in captured_output, (
        "Notifier failed to generate alert for above-threshold value"
    )


def test_division_flow(calc, log, notifier_high) -> None:
    """
    Tests the complete flow of division operations through the system.

    This test verifies that:
    1. The Calculator correctly divides one number by another (30 / 3)
    2. The Logger properly records the operation and result
    3. The Notifier behavior with a result (10) that equals the threshold (10)
       Note: The test doesn't explicitly assert notification behavior as it depends
       on whether the implementation uses > or >= for threshold checking
    """
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.divide,
        30,
        3,
        "/",
    )
    assert result == 10, f"Division calculation failed: expected 10, got {result}"
    assert "LOG: Result of 30 / 3 = 10" in captured_output, (
        "Logger failed to record division operation"
    )


def test_division_by_zero(calc, log) -> None:
    """
    Tests error handling when attempting to divide by zero.

    This test verifies that:
    1. The Calculator correctly raises a ValueError with the appropriate message
       when attempting to divide by zero
    2. The Logger is able to record error information after exceptions occur

    This test is important for validating proper error handling throughout
    the system components.
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)
        log.log("ERROR: Division by zero attempted")
        # Verify the error message was properly logged
        captured_output = mock_stdout.getvalue()
        assert "ERROR: Division by zero attempted" in captured_output, (
            "Error logging failed for division by zero"
        )


def test_below_threshold_notification(calc, log, notifier_high) -> None:
    """
    Tests that notifications are not triggered for values below the threshold.

    This test verifies that:
    1. The Calculator correctly adds two small numbers (1 + 2)
    2. The Logger properly records the operation and result
    3. The Notifier correctly identifies the result (3) as below
       the threshold (10) and does NOT generate an alert

    This test is important for ensuring the Notifier doesn't generate
    false positive alerts.
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        result = calc.add(1, 2)
        log.log(f"Result of 1 + 2 = {result}")
        # Check if notification is generated (should not be)
        notifier_high.notify(result)
        # Verify the calculation result
        captured_output = mock_stdout.getvalue()
        assert result == 3, f"Addition calculation failed: expected 3, got {result}"
        # Verify no alert was generated since 3 < 10 (threshold)
        assert "ALERT:" not in captured_output, (
            "Notifier incorrectly generated alert for below-threshold value"
        )


def test_decimal_operations(calc, log, notifier_high) -> None:
    """
    Tests the system's handling of decimal (floating-point) numbers.

    This test verifies that:
    1. The Calculator correctly adds decimal numbers (5.5 + 4.8)
    2. The Logger properly records the operation and result, including the decimal
    points
    3. The Notifier correctly identifies the result (10.3) as exceeding
       the threshold (10) and generates an alert
    """
    # Execute the decimal addition operation through the full system flow
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.add,
        5.5,
        4.8,
        "+",
    )
    assert result == 10.3, (
        f"Decimal addition calculation failed: expected 10.3, got {result}"
    )
    assert "LOG: Result of 5.5 + 4.8 = 10.3" in captured_output, (
        "Logger failed to record decimal addition operation"
    )
    # Verify the notifier generated an alert since 10.3 > 10 (threshold)
    assert "ALERT: Value 10.3 exceeded threshold 10" in captured_output, (
        "Notifier failed to generate alert for above-threshold decimal value"
    )


def test_negative_numbers(calc, log, notifier_high) -> None:
    """
    Tests the system's handling of negative numbers.

    This test verifies that:
    1. The Calculator correctly adds a negative and positive number (-15 + 5)
    2. The Logger properly records the operation and result, including the negative sign
    3. The Notifier correctly identifies the result (-10) as below
       the threshold (10) and does NOT generate an alert
    """
    captured_output, result = execute_flow(
        log,
        notifier_high,
        calc.add,
        -15,
        5,
        "+",
    )
    assert result == -10, f"Negative number addition failed: expected -10, got {result}"
    assert "LOG: Result of -15 + 5 = -10" in captured_output, (
        "Logger failed to record negative number operation"
    )
    # Verify no alert was generated since -10 < 10 (threshold)
    assert "ALERT:" not in captured_output, (
        "Notifier incorrectly generated alert for negative value below threshold"
    )


def test_complex_flow(calc, log, notifier_high, notifier_low) -> None:
    """
    Tests a complex sequence of operations that build upon previous results.

    This test verifies that:
    1. The Calculator can perform a sequence of operations where each result
       feeds into the next calculation
    2. The Logger properly records each step in the chain of operations
    3. Multiple Notifiers with different thresholds behave correctly with
       the final result

    This test simulates a more realistic usage scenario with a chain of
    calculations leading to a final result.

    The sequence is:
    1. Add 5 + 10 = 15
    2. Multiply 15 * 2 = 30
    3. Subtract 30 - 5 = 25
    4. Divide 25 / 5 = 5

    The final result (5) should be below both threshold values (10 and 100).
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        # Step 1: Perform initial addition
        result1 = calc.add(5, 10)
        log.log(f"First calculation: 5 + 10 = {result1}")

        # Step 2: Multiply the previous result by 2
        result2 = calc.multiply(result1, 2)
        log.log(f"Second calculation: {result1} * 2 = {result2}")

        # Step 3: Subtract 5 from the previous result
        result3 = calc.subtract(result2, 5)
        log.log(f"Third calculation: {result2} - 5 = {result3}")

        # Step 4: Divide the previous result by 5
        result4 = calc.divide(result3, 5)
        log.log(f"Final calculation: {result3} / 5 = {result4}")

        # Test notification with both high and low threshold notifiers
        notifier_high.notify(result4)
        notifier_low.notify(result4)

        # Verify all intermediate and final calculation results
        assert result1 == 15, f"First calculation failed: expected 15, got {result1}"
        assert result2 == 30, f"Second calculation failed: expected 30, got {result2}"
        assert result3 == 25, f"Third calculation failed: expected 25, got {result3}"
        assert result4 == 5, f"Final calculation failed: expected 5, got {result4}"

        # Capture and verify logged output
        captured_output = mock_stdout.getvalue()

        # Verify all log messages appear in the output
        assert "LOG: First calculation: 5 + 10 = 15" in captured_output, (
            "First calculation log missing"
        )
        assert "LOG: Second calculation: 15 * 2 = 30" in captured_output, (
            "Second calculation log missing"
        )
        assert "LOG: Third calculation: 30 - 5 = 25" in captured_output, (
            "Third calculation log missing"
        )
        assert "LOG: Final calculation: 25 / 5 = 5" in captured_output, (
            "Final calculation log missing"
        )

        # Verify neither notifier generated an alert since 5 < 10 and 5 < 100
        assert "ALERT: Value 5 exceeded threshold 10" not in captured_output, (
            "High threshold notifier incorrectly triggered"
        )
        assert "ALERT: Value 5 exceeded threshold 100" not in captured_output, (
            "Low threshold notifier incorrectly triggered"
        )


def test_invalid_operations(calc, log) -> None:
    """
    Tests handling of invalid input types, such as attempting to add a string to a num.

    This test verifies that:
    1. The Calculator correctly raises TypeError when given invalid inputs
       (e.g., attempting to add string and number)
    2. The Logger can still function after exceptions to record error information

    This test ensures the system handles type errors appropriately rather than
    producing unexpected results or crashing.
    """
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        # Verify TypeError is raised when attempting an operation with a string
        with pytest.raises(TypeError):
            calc.add("string", 5)

        # Verify the logger can record information about the error
        log.log("ERROR: Invalid operation with non-numeric input")

        # Verify the error message was properly logged
        captured_output = mock_stdout.getvalue()
        assert "ERROR: Invalid operation" in captured_output, (
            "Error logging failed for invalid operation"
        )
