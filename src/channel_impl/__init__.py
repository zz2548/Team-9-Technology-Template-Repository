from src import channel_api

from . import _impl

# Dependency Injection of this implementation into the API
channel_api.get_service = lambda: _impl.InMemoryChannelService()
