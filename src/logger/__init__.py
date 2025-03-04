# Import and expose the Logger class
from .logger import Logger

# Create a default instance for convenient use
default_logger = Logger()

# Expose the log method directly for simpler usage
log = default_logger.log

# Define what gets imported with "from logger_package import *"
__all__ = [
    "Logger",
    "default_logger",
    "log"
]

# Package metadata
__version__ = "0.1.0"
__authors__ = [
    {"name": "Jerry Zou", "email": "zz2548@nyu.edu"},
    {"name": "Keshav Rajput", "email": "kr3412@nyu.edu"},
    {"name": "Terry Xu", "email": "xm2204@nyu.edu"},
    {"name": "Jinglin Tao", "email": "jt4296@nyu.edu"}
]