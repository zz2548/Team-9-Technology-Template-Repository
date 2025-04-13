# No need to import pytest when only using assert statements
from src.message import Message


class MockMessage(Message):
    def __init__(self, sender_id: str, channel_id: str, content: str) -> None:
        super().__init__(sender_id, channel_id, content)

    def get_id(self) -> str:
        return "msg001"

    def get_sender(self) -> str:
        return self.sender_id

    def get_channel(self) -> str:
        return self.channel_id

    def get_content(self) -> str:
        return self.content

    @staticmethod
    def send_message(sender_id: str, channel_id: str, content: str) -> "Message":
        return MockMessage(sender_id, channel_id, content)

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list["Message"]:
        return [MockMessage("u1", channel_id, f"msg {i}") for i in range(count)]


def test_send_and_get_message() -> None:
    msg = MockMessage.send_message("u42", "general", "Hello!")
    assert msg.get_sender() == "u42"
    assert msg.get_channel() == "general"
    assert msg.get_content() == "Hello!"


def test_fetch_latest() -> None:
    msgs = MockMessage.fetch_latest("general", 3)
    assert len(msgs) == 3
    assert all(isinstance(m, MockMessage) for m in msgs)
