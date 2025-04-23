from typing import ClassVar

from src.channel_api.interfaces import ChannelEntity, ChannelService


class InMemoryChannel(ChannelEntity):
    channels_: ClassVar[dict[str, list[str]]] = {}

    def __init__(self, channel_id: str, name: str) -> None:
        self.channel_id = channel_id
        self.name = name
        self.channels_.setdefault(channel_id, [])

    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> list[str]:
        return self.channels_[self.channel_id]

class InMemoryChannelService(ChannelService):
    def create_channel(self, name: str) -> ChannelEntity:
        new_id = f"chan_{len(InMemoryChannel.channels_) + 1}"
        return InMemoryChannel(new_id, name)

    def join_channel(self, user_id: str, channel_id: str) -> bool:
        InMemoryChannel.channels_.setdefault(channel_id, [])
        if user_id not in InMemoryChannel.channels_[channel_id]:
            InMemoryChannel.channels_[channel_id].append(user_id)
        return True
