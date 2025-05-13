from typing import ClassVar, Protocol


class ChannelProtocol(Protocol):

    def get_id(self) -> str:
        ...

    def get_name(self) -> str:
        ...

    def list_users(self) -> list[str]:
        ...


class Channel:
    # mock in-memory store of users per channel
    _channels: ClassVar[dict[str, list[str]]] = {}
    # New: store channel creators
    _creators: ClassVar[dict[str, str]] = {}

    def __init__(self, channel_id: str,
                 name: str, creator_id: str | None = None) -> None:
        self.channel_id = channel_id
        self.name = name
        if channel_id not in Channel._channels:
            Channel._channels[channel_id] = []

        # Add creator if provided
        if creator_id:
            # Store the creator ID for this channel
            Channel._creators[channel_id] = creator_id
            # Ensure creator is in the channel
            if creator_id not in Channel._channels[channel_id]:
                Channel._channels[channel_id].append(creator_id)

    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> list[str]:
        return Channel._channels.get(self.channel_id, []) or []

    def get_creator(self) -> str | None:
        return Channel._creators.get(self.channel_id)

    def is_admin(self, user_id: str) -> bool:
        return user_id == self.get_creator()

    def add_user(self, user_id: str, added_by: str) -> bool:
        # Check if adder is the admin
        if not self.is_admin(added_by):
            return False

        # Add the user
        return Channel.join_channel(user_id, self.channel_id)

    def remove_user(self, user_id: str, removed_by: str) -> bool:
        # Creator/admin cannot be removed
        if user_id == self.get_creator():
            return False

        # Check if remover is the admin
        if not self.is_admin(removed_by):
            return False

        # Remove the user
        if user_id in Channel._channels[self.channel_id]:
            Channel._channels[self.channel_id].remove(user_id)
            return True
        return False

    @staticmethod
    def create_channel(name: str, creator_id: str | None = None) -> "Channel":
        new_id = f"chan_{len(Channel._channels) + 1}"
        return Channel(new_id, name, creator_id)

    @staticmethod
    def join_channel(user_id: str, channel_id: str) -> bool:
        if channel_id not in Channel._channels:
            Channel._channels[channel_id] = []
        if user_id not in Channel._channels[channel_id]:
            Channel._channels[channel_id].append(user_id)
        return True
