import sys
import os
import asyncio
from typing import Optional

# Add submodule path to sys.path for local dev (not needed in CI since it's in PYTHONPATH there)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../external/ai_convo_client")))

from ai_conversation_client.providers import OpenAIClient

class AiBotChannel:
    def __init__(self) -> None:
        self.client = OpenAIClient()
        self.conversation = self.client.create_conversation(
            title="AI Helpdesk",
            system_prompt="You are an assistant for homework and learning"
        )

    async def _ask_ai(self, message: str) -> str:
        response = await self.client.send_message(self.conversation.id, message)
        return response.content

    def handle_message(self, message: str) -> str:
        return asyncio.run(self._ask_ai(message))
