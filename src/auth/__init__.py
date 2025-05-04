"""
Authentication package for the chat application.
Provides functions for token generation, validation and user authentication.
"""

from .auth import (
    generate_token,
    decode_token,
    token_required,
    JWT_SECRET
)

# Make these functions available when importing the auth package
__all__ = [
    'generate_token',
    'decode_token',
    'token_required',
    'JWT_SECRET'
]