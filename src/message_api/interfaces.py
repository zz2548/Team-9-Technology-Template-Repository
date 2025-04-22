from typing import Protocol


class IMessage(Protocol):
    sender_id: str
    channel_id: str
    content: str

    def get_id(self) -> str: ...

    def get_sender(self) -> str: ...

    def get_channel(self) -> str: ...

    def get_content(self) -> str: ...


class IMessageService(Protocol):

    @staticmethod
    def send_message(sender_id: str, channel_id: str, content: str) -> IMessage: ...

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list[IMessage]: ...

Message = IMessage
