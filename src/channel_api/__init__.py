# src/channel_api/__init__.py
from typing import TYPE_CHECKING, cast

from src.channel_impl._impl import InMemoryChannel as _ChannelImpl

from .interfaces import ChannelEntity, ChannelService

if TYPE_CHECKING:
    from src.channel_impl._impl import InMemoryChannel as _InMemoryChannel  # noqa: F401

def _lazy_service() -> ChannelService:
    from src.channel_impl._impl import InMemoryChannelService
    return InMemoryChannelService()

_service: ChannelService = _lazy_service()

def get_service() -> ChannelService:
    return _service

Channel: type[ChannelEntity] = cast(type[ChannelEntity], _ChannelImpl)

def _create(name: str) -> ChannelEntity:
    return get_service().create_channel(name)

def _join(user_id: str, channel_id: str) -> bool:
    return get_service().join_channel(user_id, channel_id)

Channel.create_channel = staticmethod(_create)  # type: ignore[attr-defined]
Channel.join_channel   = staticmethod(_join)    # type: ignore[attr-defined]
