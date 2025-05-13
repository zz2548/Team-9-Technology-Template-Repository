import unittest

from src.channel import Channel


class MockChannel(Channel):
    def __init__(self, channel_id: str, name: str) -> None:
        super().__init__(channel_id, name)

    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> list[str]:
        return ["u1", "u2"]

    @staticmethod
    def create_channel(name: str, _creator_id: str | None = None) -> "Channel":
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

    def test_create_channel(self) -> None:
        chan = Channel.create_channel("support")
        self.assertIsInstance(chan, Channel)
        self.assertTrue(chan.get_id().startswith("chan_"))
        self.assertEqual(chan.get_name(), "support")

    def test_join_same_user_twice(self) -> None:
        chan = Channel("chan_x", "general")
        Channel.join_channel("user42", "chan_x")
        # Joining same user again
        result = Channel.join_channel("user42", "chan_x")
        self.assertTrue(result)
        self.assertEqual(chan.list_users().count("user42"), 1)  # still one instance

    def test_channel_reinit(self) -> None:
        # First init creates the entry
        Channel("chan_y", "alpha")
        # Second init shouldn't overwrite
        Channel("chan_y", "beta")
        chan = Channel("chan_y", "alpha")
        self.assertEqual(chan.get_name(), "alpha")

if __name__ == "__main__":
    unittest.main()
