import uuid
from typing import Protocol


class MessageContent(Protocol):

    def get_content_type(self) -> str:
        ...

    def get_data(self) -> dict[str, str]:
        ...


class TextContent:
    def __init__(self, text: str) -> None:
        self.text = text

    def get_content_type(self) -> str:
        return "text"

    def get_data(self) -> dict[str, str]:
        return {"text": self.text}


class ImageContent:
    def __init__(self, url: str, alt_text: str = "") -> None:
        self.url = url
        self.alt_text = alt_text

    def get_content_type(self) -> str:
        return "image"

    def get_data(self) -> dict[str, str]:
        return {"url": self.url, "alt_text": self.alt_text}


class VideoContent:
    def __init__(self, url: str, title: str = "") -> None:
        self.url = url
        self.title = title

    def get_content_type(self) -> str:
        return "video"

    def get_data(self) -> dict[str, str]:
        return {"url": self.url, "title": self.title}


class AudioContent:
    def __init__(self, url: str, title: str = "") -> None:
        self.url = url
        self.title = title

    def get_content_type(self) -> str:
        return "audio"

    def get_data(self) -> dict[str, str]:
        return {"url": self.url, "title": self.title}


class DocumentContent:
    def __init__(self, url: str, filename: str) -> None:
        self.url = url
        self.filename = filename

    def get_content_type(self) -> str:
        return "document"

    def get_data(self) -> dict[str, str]:
        return {"url": self.url, "filename": self.filename}


class ReplyContent:
    def __init__(self, text: str, reply_to_id: str) -> None:
        self.text = text
        self.reply_to_id = reply_to_id

    def get_content_type(self) -> str:
        return "reply"

    def get_data(self) -> dict[str, str]:
        return {"text": self.text, "reply_to_id": self.reply_to_id}


class Message:
    def __init__(
        self,
        sender_id: str,
        channel_id: str,
        content: MessageContent,
    ) -> None:
        self.sender_id = sender_id
        self.channel_id = channel_id
        self.content = content
        self._id = str(uuid.uuid4())

    def get_id(self) -> str:
        return self._id

    def get_sender(self) -> str:
        return self.sender_id

    def get_channel(self) -> str:
        return self.channel_id

    def get_content(self) -> MessageContent:
        return self.content

    @staticmethod
    def send_message(
        sender_id: str,
        channel_id: str,
        content: MessageContent,
    ) -> "Message":
        return Message(sender_id, channel_id, content)

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list["Message"]:
        # Creating example messages with TextContent
        return [
            Message(f"user{i}", channel_id, TextContent(f"Message {i}"))
            for i in range(count)
        ]
