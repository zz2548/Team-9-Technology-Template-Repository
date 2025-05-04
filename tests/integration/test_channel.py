"""
Integration tests for channel-related API endpoints.

These tests cover creating a channel, listing channels, joining a channel,
and retrieving users in a specific channel. They simulate client requests
to the Flask application using a test client and an in-memory database.
"""

import pytest
from flask import session
from app import app, db

# Test variables
CREATED_CHANNEL_ID = None
TEST_USER = {"username": "testuser", "password": "testpassword"}
TEST_USER_ID = None
AUTH_TOKEN = None

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a Flask test client with application context and in-memory database.

    This fixture sets up a temporary test environment for the Flask app, including
    pushing the app context and creating the in-memory database tables before
    yielding the test client. After the tests finish, it tears down the context and drops the database.
    """
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    db.create_all()

    # Register a test user that can be used for authentication
    register_response = testing_client.post("/register", json=TEST_USER)
    user_data = register_response.get_json()

    global TEST_USER_ID, AUTH_TOKEN
    TEST_USER_ID = user_data.get("user_id")
    AUTH_TOKEN = user_data.get("token")

    yield testing_client

    db.drop_all()
    ctx.pop()

@pytest.fixture(scope="function")
def authenticated_client(test_client):
    """
    Returns a test client with an authenticated session.

    This ensures the client has a valid session cookie for requests that
    require authentication via Flask-Login.
    """
    # Log in the test user to get a session cookie
    test_client.post("/login", json=TEST_USER)

    return test_client

def test_create_channel(authenticated_client):
    """Tests the creation of a new channel."""
    global CREATED_CHANNEL_ID

    response = authenticated_client.post("/channel", json={"name": "general"})
    assert response.status_code == 200

    data = response.get_json()
    assert "channel_id" in data
    assert data["name"] == "general"

    CREATED_CHANNEL_ID = data["channel_id"]

def test_list_channels(authenticated_client):
    """Tests whether all created channels are properly listed."""

    response = authenticated_client.get("/channels")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert any(channel["name"] == "general" for channel in data)

def test_join_channel(authenticated_client):
    """Tests joining a channel using the authenticated user."""
    global CREATED_CHANNEL_ID

    # Make sure we have a channel to join
    if not CREATED_CHANNEL_ID:
        # Create a channel if one wasn't created yet
        response = authenticated_client.post("/channel", json={"name": "join-test-channel"})
        data = response.get_json()
        CREATED_CHANNEL_ID = data["channel_id"]

    # No need to register a new user, use the already authenticated user
    response = authenticated_client.post("/channel/join", json={
        "channel_id": CREATED_CHANNEL_ID,
    })
    assert response.status_code == 200

    data = response.get_json()
    assert data["joined"] is True

def test_list_channel_users(authenticated_client):
    """Tests the retrieval of users in a specific channel."""
    global CREATED_CHANNEL_ID

    # Ensure CREATED_CHANNEL_ID is available
    if not CREATED_CHANNEL_ID:
        # Create a channel if one wasn't created yet
        response = authenticated_client.post("/channel", json={"name": "test-channel"})
        data = response.get_json()
        CREATED_CHANNEL_ID = data["channel_id"]

        # Join the channel
        authenticated_client.post("/channel/join", json={
            "channel_id": CREATED_CHANNEL_ID,
        })

    response = authenticated_client.get(f"/channel/{CREATED_CHANNEL_ID}/users")
    assert response.status_code == 200

    data = response.get_json()
    assert "users" in data
    assert isinstance(data["users"], list)

    # Verify our test user is in the list
    user_ids = [user.get("id") for user in data["users"]]
    assert TEST_USER_ID in user_ids

# Alternative approach using JWT token authentication
def test_api_create_channel_with_token():
    """Tests creating a channel using token authentication."""
    global AUTH_TOKEN

    # Create a new test client for this test
    client = app.test_client()

    # Use the token from the registered user
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

    response = client.post(
        "/channel",
        json={"name": "token-auth-channel"},
        headers=headers
    )
    assert response.status_code == 200

    data = response.get_json()
    assert "channel_id" in data
    assert data["name"] == "token-auth-channel"