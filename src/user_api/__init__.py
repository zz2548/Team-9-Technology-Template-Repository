# src/user_api/__init__.py
from typing import TYPE_CHECKING

from .interfaces import IUser, IUserService

__all__ = [
    "IUser",
    "IUserService",
    "User",
    "get_service",
]

from src.user_impl._impl import User as _ImplUser
from src.user_impl._impl import UserService as _ImplService

_service = _ImplService()

def get_service() -> IUserService:
    return _service

User = _ImplUser

if not TYPE_CHECKING:
    User.register = staticmethod(lambda username: _service.register(username))  # type: ignore[attr-defined]
    User.login    = staticmethod(lambda username: _service.login(username))     # type: ignore[attr-defined]
