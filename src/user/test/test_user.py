import unittest

from src.user import User


class MockUser(User):
    def __init__(self, user_id: str, username: str) -> None:
        super().__init__(user_id, username)

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> list[str]:
        return ["general", "random"]

    @staticmethod
    def register(username: str) -> "User":
        return MockUser("u123", username)

    @staticmethod
    def login(username: str) -> "User":
        return MockUser("u123", username)

class TestUserAPI(unittest.TestCase):
    def test_register_and_login(self) -> None:
        user = MockUser.register("alice")
        self.assertEqual(user.get_username(), "alice")

        logged_in = MockUser.login("alice")
        self.assertEqual(logged_in.get_username(), "alice")

    def test_list_channels(self) -> None:
        user = MockUser("u123", "bob")
        channels = user.list_channels()
        self.assertIn("general", channels)

    def test_register_user(self) -> None:
        user = User.register("charlie")
        self.assertIsInstance(user, User)
        self.assertEqual(user.get_username(), "charlie")

    def test_login_user(self) -> None:
        user = User.login("charlie")
        self.assertIsInstance(user, User)
        self.assertEqual(user.get_username(), "charlie")

    def test_user_getters(self) -> None:
        user = User("u001", "charlie")
        self.assertEqual(user.get_id(), "u001")
        self.assertEqual(user.get_username(), "charlie")



if __name__ == "__main__":
    unittest.main()
