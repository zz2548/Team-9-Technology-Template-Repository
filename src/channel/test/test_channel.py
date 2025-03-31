import unittest
from src.channel import Channel

class MockChannel(Channel):
    def __init__(self, channel_id: str, name: str) -> None:
        super().__init__(channel_id, name)
        
    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> List[str]:
        return ["u1", "u2"]

    @staticmethod
    def create_channel(name: str) -> 'Channel':
        return MockChannel("c123", name)

    @staticmethod
    def join_channel(_user_id: str, _channel_id: str) -> bool:
        return True

class TestChannelAPI(unittest.TestCase):
    def test_create_and_get_channel(self) -> None:
        chan = MockChannel.create_channel("general")
        self.assertEqual(chan.get_name(), "general")

    def test_join_channel(self) -> None:
        result = MockChannel.join_channel("u42", "general")
        self.assertTrue(result)

    def test_list_users(self) -> None:
        chan = MockChannel("c1", "general")
        users = chan.list_users()
        self.assertIn("u1", users)

if __name__ == '__main__':
    unittest.main()
