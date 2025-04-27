import sys
import os
import asyncio
import re
from pathlib import Path
from typing import cast, Optional, Tuple

# add submodule path to sys.path for local dev
current_file = Path(__file__).resolve()
ai_module_path = current_file.parent.parent.parent / "external" / "ai_convo_client"
issue_tracker_path = current_file.parent.parent.parent / "external" / "issue_tracker"
sys.path.append(str(ai_module_path))
sys.path.append(str(issue_tracker_path))


from ai_conversation_client.providers import OpenAIClient # type: ignore[import-not-found]
from api.src.issue_tracker import MemoryIssueTrackerClient

class AiBotChannel:
    def __init__(self) -> None:
        self.client = OpenAIClient()
        self.issue_tracker = MemoryIssueTrackerClient()
        self.conversation = self.client.create_conversation(
            title="AI Helpdesk",
            system_prompt=(
               "You are an assistant for homework and learning. "
               "You can also create tasks in the issue tracker when requested. "
               "If a user asks to create a task, respond confirming the task was created."
                )
        )

    async def _ask_ai(self, message: str) -> str:
        """
        Process a message, extract task info if present, and append task list to response.
        Verbose version with detailed logging for Flask.
        """
        from flask import current_app

        # Log the incoming message
        current_app.logger.info(f"Processing message: {message[:50]}...")

        # Extract task info if present
        task_info = self._extract_task_info(message)
        if task_info:
            # Create the task
            title, description = task_info
            current_app.logger.info(
                f"Creating task with title: '{title}' and description: '{description}'")

            try:
                issue = self.issue_tracker.create_issue(title=title,
                                                        description=description)
                current_app.logger.info(
                    f"Task created successfully with ID: {issue.id}")

                # Modify the message to inform AI about task creation
                task_creation_note = f"\n[System: Task '{title}' has been created with ID: {issue.id}]"
                message += task_creation_note
                current_app.logger.info(
                    f"Added task creation note to message: {task_creation_note}")
            except Exception as e:
                current_app.logger.error(f"Failed to create task: {str(e)}")
                # Continue with original message if task creation fails
        else:
            current_app.logger.info("No task creation request found in message")

        # Send the message to AI
        current_app.logger.info(
            f"Sending message to AI conversation ID: {self.conversation.id}")
        try:
            response = await self.client.send_message(self.conversation.id, message)
            current_app.logger.info("Received response from AI")

            # Get response content
            response_content = cast(str, response.content)
            content_preview = response_content[:50] + "..." if len(
                response_content) > 50 else response_content
            current_app.logger.info(f"Response content preview: {content_preview}")
        except Exception as e:
            current_app.logger.error(f"Error getting response from AI: {str(e)}")
            return f"Error communicating with AI assistant: {str(e)}"

        # Get current tasks and append them to the response
        current_app.logger.info("Retrieving current tasks from issue tracker")
        try:
            tasks = list(self.issue_tracker.get_issues())
            current_app.logger.info(f"Retrieved {len(tasks)} tasks from issue tracker")

            if tasks:
                tasks_info = "\n\nCurrent Tasks:\n"
                for task in tasks:
                    task_line = f"- {task.id}: {task.title}\n"
                    tasks_info += task_line
                    current_app.logger.info(f"Added task to list: {task_line.strip()}")

                final_response = response_content + tasks_info
                current_app.logger.info(
                    f"Appended task list ({len(tasks)} tasks) to response")
                current_app.logger.debug(
                    f"Final response length: {len(final_response)} characters")

                return final_response
            else:
                current_app.logger.info("No tasks found, returning original response")
                return response_content
        except Exception as e:
            current_app.logger.error(f"Error retrieving or formatting tasks: {str(e)}")
            # Return just the AI response if there's an error with tasks
            return response_content



    def _extract_task_info(self, message: str) -> Optional[Tuple[str, str]]:
        """Extract task title and description from message."""
        # Check if message contains task creation request
        if "create a task" not in message.lower():
            return None

        # Basic regex pattern to extract task details
        # Format expected: create a task "title" "description"
        pattern = r'create a task\s+"([^"]+)"\s+"([^"]*)"'
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            title = match.group(1).strip()
            description = match.group(2).strip()
            return title, description

    def handle_message(self, message: str) -> str:
        return asyncio.run(self._ask_ai(message))
