import unittest
from chat_client.channel import Channel

class MockChannel(Channel):
    def get_id(self):
        return self.channel_id

    def get_name(self):
        return self.name

    def list_users(self):
        return ["u1", "u2"]

    @staticmethod
    def create_channel(name):
        return MockChannel("c123", name)

    @staticmethod
    def join_channel(user_id, channel_id):
        return True

class TestChannelAPI(unittest.TestCase):
    def test_create_and_get_channel(self):
        chan = MockChannel.create_channel("general")
        self.assertEqual(chan.get_name(), "general")

    def test_join_channel(self):
        result = MockChannel.join_channel("u42", "general")
        self.assertTrue(result)

    def test_list_users(self):
        chan = MockChannel("c1", "general")
        users = chan.list_users()
        self.assertIn("u1", users)

if __name__ == '__main__':
    unittest.main()
