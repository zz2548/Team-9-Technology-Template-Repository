# Import and expose the Calculator class
from .calculator import Calculator

# Create a default instance for convenient use
default_calculator = Calculator()

# You can also expose specific methods directly for even simpler usage
add = default_calculator.add
subtract = default_calculator.subtract
multiply = default_calculator.multiply
divide = default_calculator.divide

# Define what gets imported with "from package import *"
__all__ = [
    "Calculator",
    "add",
    "default_calculator",
    "divide",
    "multiply",
    "subtract",
]

# Package metadata
__version__ = "0.1.0"
