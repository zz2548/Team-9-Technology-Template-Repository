
from src.message_api import IMessage, IMessageService


class Message(IMessage):
    def __init__(self, sender_id: str, channel_id: str, content: str) -> None:
        self.sender_id = sender_id
        self.channel_id = channel_id
        self.content = content
        self._id = f"{sender_id}_{channel_id}_001"

    def get_id(self) -> str:
        return self._id

    def get_sender(self) -> str:
        return self.sender_id

    def get_channel(self) -> str:
        return self.channel_id

    def get_content(self) -> str:
        return self.content

class MessageService(IMessageService):
    @staticmethod
    def send_message(sender_id: str, channel_id: str, content: str) -> IMessage:
        return Message(sender_id, channel_id, content)

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list[IMessage]:
        return [Message(f"user{i}", channel_id, f"Message {i}") for i in range(count)]
