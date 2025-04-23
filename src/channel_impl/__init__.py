import src.channel_api as api

from ._impl import InMemoryChannelService

api.get_service = lambda: InMemoryChannelService()   # 依赖注入
