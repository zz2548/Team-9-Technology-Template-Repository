# Import and expose the Notifier class
from .notifier import Notifier

# Unlike Logger and Calculator, Notifier requires a threshold parameter,
# so we don't create a default instance automatically

# Define what gets imported with "from notifier_package import *"
__all__ = [
    "Notifier"
]

# Package metadata
__version__ = "0.1.0"
__authors__ = [
    {"name": "Jerry Zou", "email": "zz2548@nyu.edu"},
    {"name": "Keshav Rajput", "email": "kr3412@nyu.edu"},
    {"name": "Terry Xu", "email":