# ruff: noqa: SLF001

import pytest
import asyncio
from unittest.mock import patch
from src.channel_impl import IssueTrackerSingleton, AIBotChannel


class MockIssueTracker:
    def __init__(self) -> None:
        self.issues = []
        self.next_id = 1

    def create_issue(self, title, description):
        issue = type('Issue', (object,), {'id': self.next_id, 'title': title, 'description': description})()
        self.issues.append(issue)
        self.next_id += 1
        return issue

    def get_issues(self):
        return self.issues


class MockAIClient:
    def __init__(self) -> None:
        self.messages_sent = []
        self.conversations = []

    def create_conversation(self, _title, _system_prompt) -> object:
        convo = type('Conversation', (object,), {'id': 'mock-id'})()
        self.conversations.append(convo)
        return convo

    async def send_message(self, conversation_id, message):
        self.messages_sent.append((conversation_id, message))
        return type('Response', (object,), {'content': 'mock response'})()


@pytest.fixture
def bot():
    with patch('src.channel_impl.IssueTrackerSingleton.get_instance', return_value=MockIssueTracker()), \
         patch('src.channel_impl.OpenAIClient', new=MockAIClient):
        return AIBotChannel()


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
