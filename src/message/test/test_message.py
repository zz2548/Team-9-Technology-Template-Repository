import unittest

from src.message import Message, MessageContent, TextContent


class MockMessage(Message):
    def __init__(self, sender_id: str,
                 channel_id: str, content: MessageContent) -> None:
        super().__init__(sender_id, channel_id, content)

    @classmethod
    def from_str(cls, sender_id: str,
                 channel_id: str, content_str: str) -> "MockMessage":
        return cls(sender_id, channel_id, TextContent(content_str))

    @staticmethod
    def send_message(sender_id: str,
                     channel_id: str, content: MessageContent) -> "Message":
        return MockMessage(sender_id, channel_id, content)

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list["Message"]:
        return [
            MockMessage.from_str("u1", channel_id, f"msg {i}")
            for i in range(count)
        ]


class TestMessageAPI(unittest.TestCase):
    def test_send_and_get_message(self) -> None:
        msg = MockMessage.from_str("u42", "general", "Hello!")
        self.assertEqual(msg.get_sender(), "u42")
        self.assertEqual(msg.get_channel(), "general")
        self.assertEqual(msg.get_content().get_data()["text"], "Hello!")

    def test_fetch_latest(self) -> None:
        msgs = MockMessage.fetch_latest("general", 3)
        self.assertEqual(len(msgs), 3)
        self.assertTrue(all(isinstance(m, MockMessage) for m in msgs))


if __name__ == "__main__":
    unittest.main()
