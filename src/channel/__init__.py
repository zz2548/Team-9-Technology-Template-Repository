from typing import ClassVar

class Channel:
    
     # mock in-memory store of users per channel
    _channels: ClassVar[dict[str, list[str]]] = {}

    def __init__(self, channel_id: str, name: str) -> None:
        self.channel_id = channel_id
        self.name = name
        if channel_id not in Channel._channels:
            Channel._channels[channel_id] = []

    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> list[str]:
        return Channel._channels.get(self.channel_id, []) or []


    @staticmethod
    def create_channel(name: str) -> 'Channel':
        new_id = f"chan_{len(Channel._channels) + 1}"
        return Channel(new_id, name)

    @staticmethod
    def join_channel(user_id: str, channel_id: str) -> bool:
        if channel_id not in Channel._channels:
            Channel._channels[channel_id] = []
        if user_id not in Channel._channels[channel_id]:
            Channel._channels[channel_id].append(user_id)
        return True
