import unittest
from typing import List
from chat_client.user import User

class MockUser(User):
    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> List[str]:
        return ["general", "random"]

    @staticmethod
    def register(username: str) -> 'MockUser':
        return MockUser("u123", username)

    @staticmethod
    def login(username: str) -> 'MockUser':
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

if __name__ == '__main__':
    unittest.main()
