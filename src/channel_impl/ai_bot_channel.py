import sys
import os
import asyncio

# Add the submodule to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../external/ai_convo_client")))

from ai_conversation_client.providers import OpenAIClient

class AiBotChannel:
    def __init__(self):
        self.client = OpenAIClient()
        self.conversation = self.client.create_conversation(
            title="AI Helpdesk",
            system_prompt="Helpful assistant for homework and task management."
        )

    async def _ask_ai(self, message):
        response = await self.client.send_message(self.conversation.id, message)
        return response.content

    def handle_message(self, message):
        return asyncio.run(self._ask_ai(message))
