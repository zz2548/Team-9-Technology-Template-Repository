from collections.abc import Sequence
from typing import ClassVar

from src.user_api.interfaces import IUser, IUserService


class User(IUser):
    """In-memory user entity that matches the original twoarg signature."""

    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> Sequence[str]:
        return ["general", "random"]


class UserService(IUserService):
    """Simple in-memory user service with incremental IDs."""

    _counter: ClassVar[int] = 0

    @classmethod
    def _next_id(cls) -> str:
        cls._counter += 1
        return f"u{cls._counter:03d}"

    def register(self, username: str) -> User:
        return User(self._next_id(), username)

    def login(self, username: str) -> User:
        # In this mock, login also issues a new ID each time.
        return User(self._next_id(), username)
