# No need to import pytest when only using assert statements
from src.user_api import User


class MockUser(User):
    def __init__(self, user_id: str, username: str) -> None:
        super().__init__(user_id, username)
        self.password_hash = None

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> list[str]:
        return ["general", "random"]

    def set_password(self, password: str) -> None:
        # This is a mock method, so we don't actually hash the password
        self.password_hash = f"mock_hash_{password}"

    def check_password(self, password: str) -> bool:
        # For testing purposes, just check if it matches our simple mock pattern
        return self.password_hash == f"mock_hash_{password}" if self.password_hash else False

    @staticmethod
    def register(username: str) -> "User":
        # Keep the original signature
        user = MockUser("u123", username)
        return user

    @staticmethod
    def login(username: str) -> "User":
        # Keep the original signature
        user = MockUser("u123", username)
        return user


def test_register_and_login() -> None:
    user = MockUser.register("alice")
    assert user.get_username() == "alice"

    logged_in = MockUser.login("alice")
    assert logged_in.get_username() == "alice"


def test_list_channels() -> None:
    user = MockUser("u123", "bob")
    channels = user.list_channels()
    assert "general" in channels


def test_register_user() -> None:
    user = User.register("charlie")
    assert isinstance(user, User)
    assert user.get_username() == "charlie"


def test_login_user() -> None:
    user = User.login("charlie")
    assert isinstance(user, User)
    assert user.get_username() == "charlie"


def test_user_getters() -> None:
    user = User("u001", "charlie")
    assert user.get_id() == "u001"
    assert user.get_username() == "charlie"