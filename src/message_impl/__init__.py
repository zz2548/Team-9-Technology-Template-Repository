from src.message_api import IMessage, IMessageService

from ._impl import Message, MessageService

__all__ = ["IMessage", "IMessageService", "Message", "MessageService"]

def get_message_service() -> type[MessageService]:
    return MessageService
