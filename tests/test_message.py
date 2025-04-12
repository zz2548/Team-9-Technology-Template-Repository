import json
import pytest
from app.models import Message


def test_get_messages(logged_in_user1):
    """Test getting messages from a channel."""
    response = logged_in_user1.get('/api/channels/1/messages')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'messages' in data
    assert len(data['messages']) == 1  # Channel 1 has 1 test message
    assert data['messages'][0]['content'] == 'Test message 1 in channel 1'
    assert data['messages'][0]['user_id'] == 1
    assert data['messages'][0]['channel_id'] == 1


def test_get_messages_from_group_channel(logged_in_user1):
    """Test getting messages from a group channel with multiple messages."""
    response = logged_in_user1.get('/api/channels/2/messages')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'messages' in data
    assert len(data['messages']) == 2  # Channel 2 has 2 test messages

    # Check message content (messages come in reverse order by default)
    contents = [msg['content'] for msg in data['messages']]
    assert 'Test message 2 in channel 2' in contents
    assert 'Test message from user 2 in channel 2' in contents


def test_get_messages_from_direct_channel(logged_in_user1):
    """Test getting messages from a direct message channel."""
    response = logged_in_user1.get('/api/channels/3/messages')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'messages' in data
    assert len(data['messages']) == 1
    assert data['messages'][0]['content'] == 'Direct message from user 1 to user 2'


def test_get_messages_unauthorized(logged_in_user2):
    """Test getting messages from a channel the user isn't a member of."""
    response = logged_in_user2.get('/api/channels/1/messages')

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'You are not a member of this channel'


def test_create_message(logged_in_user1):
    """Test creating a new message in a channel."""
    response = logged_in_user1.post(
        '/api/channels/1/messages',
        json={'content': 'New test message'},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Message sent successfully'
    assert 'data' in data
    assert data['data']['content'] == 'New test message'
    assert data['data']['user_id'] == 1
    assert data['data']['channel_id'] == 1

    # Verify message was created
    response = logged_in_user1.get('/api/channels/1/messages')
    data = json.loads(response.data)
    assert len(data['messages']) == 2  # Now there should be 2 messages


def test_create_message_validation(logged_in_user1):
    """Test validation when creating a message."""
    # Test empty content
    response = logged_in_user1.post(
        '/api/channels/1/messages',
        json={'content': ''},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Message content is required'

    # Test whitespace-only content
    response = logged_in_user1.post(
        '/api/channels/1/messages',
        json={'content': '   '},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Message content is required'


def test_create_message_unauthorized(logged_in_user2):
    """Test creating a message in a channel the user isn't a member of."""
    response = logged_in_user2.post(
        '/api/channels/1/messages',
        json={'content': 'This should fail'},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'You are not a member of this channel'


def test_update_message(logged_in_user1, app):
    """Test updating a message."""
    with app.app_context():
        # Get message ID
        message = Message.query.filter_by(channel_id=1).first()
        message_id = message.id

    response = logged_in_user1.put(
        f'/api/messages/{message_id}',
        json={'content': 'Updated message content'},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Message updated successfully'
    assert 'data' in data
    assert data['data']['content'] == 'Updated message content'

    # Verify message was updated
    response = logged_in_user1.get('/api/channels/1/messages')
    data = json.loads(response.data)
    assert data['messages'][0]['content'] == 'Updated message content'


def test_update_message_unauthorized(logged_in_user2, app):
    """Test updating someone else's message."""
    with app.app_context():
        # Get message ID for a message from user 1
        message = Message.query.filter_by(user_id=1, channel_id=2).first()
        message_id = message.id

    response = logged_in_user2.put(
        f'/api/messages/{message_id}',
        json={'content': 'This should fail'},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'You can only edit your own messages'


def test_delete_message(logged_in_user1, app):
    """Test deleting a message."""
    with app.app_context():
        # Create a new message to delete
        db = app.extensions['sqlalchemy'].db
        new_message = Message(
            content='Message to delete',
            user_id=1,
            channel_id=1
        )
        db.session.add(new_message)
        db.session.commit()
        message_id = new_message.id

    # Delete the message
    response = logged_in_user1.delete(f'/api/messages/{message_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Message deleted successfully'

    # Verify the message was deleted
    with app.app_context():
        message = Message.query.get(message_id)
        assert message is None


def test_delete_other_user_message_as_channel_owner(logged_in_user1, app):
    """Test deleting another user's message as the channel owner."""
    with app.app_context():
        # Get message ID for a message from user 2 in channel 2
        # User 1 is the owner of channel 2
        message = Message.query.filter_by(user_id=2, channel_id=2).first()
        message_id = message.id

    response = logged_in_user1.delete(f'/api/messages/{message_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Message deleted successfully'


def test_delete_message_unauthorized(logged_in_user2, app):
    """Test deleting someone else's message without being the channel owner."""
    with app.app_context():
        # Get message ID for a message from user 1 in channel 1
        # User 2 is not a member of channel 1
        message = Message.query.filter_by(channel_id=1).first()
        message_id = message.id

    response = logged_in_user2.delete(f'/api/messages/{message_id}')

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'You cannot delete this message'

