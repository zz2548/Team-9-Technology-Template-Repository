import sys
import os
import asyncio
from typing import Optional
from typing import cast
from pathlib import Path

# add submodule path to sys.path for local dev (not needed in CI since it's in PYTHONPATH there)
current_file = Path(__file__).resolve()
submodule_path = current_file.parent.parent.parent / "external" / "ai_convo_client"
sys.path.append(str(submodule_path))

from ai_conversation_client.providers import OpenAIClient # type: ignore[import-not-found]

class AiBotChannel:
    def __init__(self) -> None:
        self.client = OpenAIClient()
        self.conversation = self.client.create_conversation(
            title="AI Helpdesk",
            system_prompt="You are an assistant for homework and learning"
        )

    async def _ask_ai(self, message: str) -> str:
        response = await self.client.send_message(self.conversation.id, message)
        return cast(str, response.content)

    def handle_message(self, message: str) -> str:
        return asyncio.run(self._ask_ai(message))
