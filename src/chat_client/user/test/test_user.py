import unittest
from chat_client.user import User

class MockUser(User):
    def get_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def list_channels(self):
        return ["general", "random"]

    @staticmethod
    def register(username):
        return MockUser("u123", username)

    @staticmethod
    def login(username):
        return MockUser("u123", username)

class TestUserAPI(unittest.TestCase):
    def test_register_and_login(self):
        user = MockUser.register("alice")
        self.assertEqual(user.get_username(), "alice")

        logged_in = MockUser.login("alice")
        self.assertEqual(logged_in.get_username(), "alice")

    def test_list_channels(self):
        user = MockUser("u123", "bob")
        self.assertIn("general", user.list_channels())

if __name__ == '__main__':
    unittest.main()
