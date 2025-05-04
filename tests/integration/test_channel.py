"""
Integration tests for channel-related API endpoints.

These tests cover creating a channel, listing channels, joining a channel,
and retrieving users in a specific channel. They simulate client requests
to the Flask application using a test client and an in-memory database.
"""

import pytest

from app import app, db

CREATED_CHANNEL_ID = None

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a Flask test client with application context and in-memory database.

    This fixture sets up a temporary test environment for the Flask app, including
    pushing the app context and creating the in-memory database tables before
    yielding the test client. After the tests finish, it tears down the context and drops the database.
    """
    
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client

    db.drop_all()
    ctx.pop()

def test_create_channel(test_client):
    """Tests the creation of a new channel."""
    
    response = test_client.post("/channel", json={"name": "general"})
    assert response.status_code == 200

    data = response.get_json()
    assert "channel_id" in data
    assert data["name"] == "general"

    global created_channel_id                   # noqa: PLW0603
    # only ignore this warning in this test file
    created_channel_id = data["channel_id"]

def test_list_channels(test_client):
    """Tests whether all created channels are properly listed."""
    
    response = test_client.get("/channels")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert any(channel["name"] == "general" for channel in data)

def test_join_channel(test_client):
    """Tests user registration and joining a channel."""
    
    register_resp = test_client.post("/register", json={"username": "charlie"})
    assert register_resp.status_code == 200
    user_data = register_resp.get_json()
    user_id = user_data["user_id"]

    response = test_client.post("/channel/join", json={
        "user_id": user_id,
        "channel_id": created_channel_id,
    })
    assert response.status_code == 200

    data = response.get_json()
    assert data["joined"] is True

def test_list_channel_users(test_client):
    """Tests the retrieval of users in a specific channel."""
    
    response = test_client.get(f"/channel/{created_channel_id}/users")
    assert response.status_code == 200

    data = response.get_json()
    assert "users" in data
    assert isinstance(data["users"], list)
