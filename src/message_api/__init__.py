from collections.abc import Sequence

from .interfaces import IMessage, IMessageService

__all__ = [
    "IMessage",
    "IMessageService",
    "Message",
    "get_service",
]

from src.message_impl._impl import Message as _ImplMessage
from src.message_impl._impl import MessageService as _ImplService

_service = _ImplService()

def get_service() -> IMessageService:
    return _service

Message = _ImplMessage

def _send(sender_id: str, channel_id: str, content: str) -> IMessage:
    return _service.send_message(sender_id, channel_id, content)

def _fetch(channel_id: str, count: int) -> Sequence[IMessage]:
    return _service.fetch_latest(channel_id, count)

Message.send_message = staticmethod(_send)  # type: ignore[attr-defined]
Message.fetch_latest = staticmethod(_fetch)  # type: ignore[attr-defined]
