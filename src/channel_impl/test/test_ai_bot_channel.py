# ruff: noqa: SLF001, ARG001, ARG002
# ARG001 and ARG002 since the unused parameters are expected in a mock class

import pytest
import asyncio
import sys
from unittest.mock import MagicMock
from unittest.mock import patch
sys.modules['ai_conversation_client'] = MagicMock()
sys.modules['ai_conversation_client.providers'] = MagicMock()
from src.channel_impl.ai_bot_channel import IssueTrackerSingleton, AiBotChannel
import pytest
from flask import Flask, current_app

@pytest.fixture
def app_context():
    app = Flask(__name__)
    with app.app_context():
        yield

@pytest.fixture
def bot(app_context):
    with patch('src.channel_impl.ai_bot_channel.IssueTrackerSingleton.get_instance', return_value=MockIssueTracker()), \
         patch('src.channel_impl.ai_bot_channel.OpenAIClient', new=MockAIClient):
        yield AiBotChannel()

@pytest.mark.asyncio
async def test_ask_ai_task(bot):
    result = await bot._ask_ai('create a task Integration "Finish integration assignment"')
    assert bot.issue_tracker.issues != []
    assert bot.issue_tracker.issues[0].title == "Integration"
    assert "Task 'Integration' has been created" in result
    assert "- 1: Integration" in result


@pytest.mark.asyncio
async def test_ask_ai_no_task(bot):
    result = await bot._ask_ai("Hello, how are you?")
    assert bot.issue_tracker.issues == []
    assert "mock response" in result
    assert "Task" not in result

class MockIssueTracker:
    def __init__(self) -> None:
        self.issues = []

    def create_issue(self, title, description):
        # Create a mock issue with an id
        issue_id = len(self.issues) + 1
        mock_issue = type('MockIssue', (),
                          {'id': issue_id, 'title': title, 'description': description})
        self.issues.append(mock_issue)
        return mock_issue

    def get_issues(self):
        return self.issues


class MockAIClient:
    def __init__(self) -> None:
        self.messages = []

    def create_conversation(self, title=None, system_prompt=None):
        # Create a simple mock conversation object with an id
        return type('MockConversation', (), {'id': '12345'})

    async def send_message(self, conversation_id, message):
        self.messages.append(message)
        # Check if this is a task creation request
        if "create a task" in message.lower():
            # Extract task name from the message
            import re
            match = re.search(r'create a task\s+(\S+)', message, re.IGNORECASE)
            task_name = match.group(1) if match else "Unknown"
            # Return a response that includes the task creation confirmation
            mock_response = type('MockResponse', (), {
                'content': f"Task '{task_name}' has been created with mock response"
            })
        else:
            # Return a default mock response
            mock_response = type('MockResponse', (), {
                'content': "mock response"
            })
        return mock_response


def test_extract_task_info_match(bot):
    message = 'create a task Integration "Complete integration assignment"'
    result = bot._extract_task_info(message)
    assert result == ("Integration", "Complete integration assignment")


def test_extract_info_no_match(bot):
    message = "empty"
    result = bot._extract_task_info(message)
    assert result is None


def test_handle_message(bot):
    with patch('asyncio.run', return_value="Mock Response") as mock_run:
        response = bot.handle_message("Hello")
        mock_run.assert_called_once()
        assert response == "Mock Response"
