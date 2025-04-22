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

def _register(username: str) -> IUser:
    return _service.register(username)

def _login(username: str) -> IUser:
    return _service.login(username)

User.register = staticmethod(_register)
User.login = staticmethod(_login)
