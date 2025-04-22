from typing import Protocol, runtime_checkable


@runtime_checkable
class ChannelEntity(Protocol):
    @property
    def get_id(self) -> str:
        raise NotImplementedError

    @property
    def get_name(self) -> str:
        raise NotImplementedError

    @property
    def list_users(self) -> list[str]:
        raise NotImplementedError


@runtime_checkable
class ChannelService(Protocol):
    @property
    def create_channel(self) -> ChannelEntity:
        raise NotImplementedError

    @property
    def join_channel(self) -> bool:
        raise NotImplementedError


def get_service() -> ChannelService:
    raise NotImplementedError("This should be injected from the impl module.")

try:
    from src.channel_impl._impl import InMemoryChannel, InMemoryChannelService

    def get_service() -> ChannelService:
        return InMemoryChannelService()

    Channel = InMemoryChannel

    Channel.create_channel = staticmethod(lambda name:
                                          get_service().create_channel(name))
    Channel.join_channel   = staticmethod(lambda uid, cid:
                                          get_service().join_channel(uid, cid))

except ImportError:
    pass
