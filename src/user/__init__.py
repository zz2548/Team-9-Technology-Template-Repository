import uuid
from typing import Protocol


# Define the User Protocol interface
class UserProtocol(Protocol):

    def get_id(self) -> str:
        ...

    def get_username(self) -> str:
        ...

    def list_channels(self) -> list[str]:
        ...


# Concrete implementation of a regular user
class User:
    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> list[str]:
        return ["general", "random"]

    @staticmethod
    def register(username: str) -> "User":
        return User(str(uuid.uuid4()), username)

    @staticmethod
    def login(username: str) -> "User":
        return User(str(uuid.uuid4()), username)


class AdminUser:
    def __init__(self, admin_id: str, username: str) -> None:
        self.admin_id = admin_id
        self.username = username
        self.admin_level = 1

    def get_id(self) -> str:
        return self.admin_id

    def get_username(self) -> str:
        return f"Admin: {self.username}"

    def list_channels(self) -> list[str]:
        # Admins have access to more channels
        return ["general", "random", "admin", "moderation"]

    def set_admin_level(self, level: int) -> None:
        self.admin_level = level
