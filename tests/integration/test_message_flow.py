import pytest

from app import app, db


@pytest.fixture(scope="module")
def test_client():
    """Create a Flask test client and initialize the database."""
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client

    db.drop_all()
    ctx.pop()

@pytest.fixture(scope="module")
def setup_users_and_channel(test_client):
    """Register users and create a normal channel."""
    # Register two users
    user1 = test_client.post("/register", json={"username": "user1"}).get_json()
    user2 = test_client.post("/register", json={"username": "user2"}).get_json()

    # Create a regular channel
    channel_resp = test_client.post("/channel", json={"name": "general"})
    channel_id = channel_resp.get_json()["channel_id"]

    return user1["user_id"], user2["user_id"], channel_id

def test_send_message(test_client, setup_users_and_channel):
    """Test sending a message to a regular channel."""
    sender_id, _, channel_id = setup_users_and_channel

    response = test_client.post("/message", json={
        "sender_id": sender_id,
        "channel_id": channel_id,
        "content": "Hello, world!",
    })
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["content"] == "Hello, world!"
    assert data[0]["sender_id"] == sender_id

def test_fetch_messages(test_client, setup_users_and_channel):
    """Test fetching messages from a channel."""
    _, _, channel_id = setup_users_and_channel

    response = test_client.get(f"/message/{channel_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Should have at least the message sent in previous test
    assert "content" in data[0]
    assert "sender_id" in data[0]


@pytest.fixture(scope="module")
def setup_ai_helpdesk_channel(test_client):
    """Create a special 'ai-helpdesk' channel."""
    ai_channel_resp = test_client.post("/channel", json={"name": "ai-helpdesk"})
    ai_channel_id = ai_channel_resp.get_json()["channel_id"]

    return ai_channel_id


def test_send_message_to_ai_bot(test_client, setup_users_and_channel, setup_ai_helpdesk_channel):
    """Test sending a message to 'ai-helpdesk' and receiving an AI bot reply."""
    sender_id, _, _ = setup_users_and_channel
    ai_channel_id = setup_ai_helpdesk_channel

    response = test_client.post("/message", json={
        "sender_id": sender_id,
        "channel_id": ai_channel_id,
        "content": "What is the weather today?"
    })
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2  # Should have original + bot reply

    assert data[0]["sender_id"] == sender_id
    assert data[1]["sender_id"] == "ai_bot"
    assert "content" in data[1]


def test_start_direct_message(test_client, setup_users_and_channel):
    """Test starting a direct message (DM) channel between two users."""
    sender_id, receiver_id, _ = setup_users_and_channel

    response = test_client.post("/start_dm", json={
        "sender_id": sender_id,
        "receiver_id": receiver_id,
    })
    assert response.status_code == 200

    data = response.get_json()
    assert "channel_id" in data
