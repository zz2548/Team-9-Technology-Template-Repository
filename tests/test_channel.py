import json
import pytest
from app.models import Channel, User


def test_get_channels(logged_in_user1):
    """Test getting channels."""
    response = logged_in_user1.get('/api/channels')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'channels' in data
    assert len(data['channels']) == 3  # Test user is in 3 channels

    # Check for expected channel names
    channel_names = [channel['name'] for channel in data['channels']]
    assert 'Test Channel 1' in channel_names
    assert 'Test Channel 2' in channel_names
    assert 'DM: testuser1 & testuser2' in channel_names


def test_get_channels_as_different_user(logged_in_user2):
    """Test getting channels as the second user."""
    response = logged_in_user2.get('/api/channels')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'channels' in data
    assert len(data['channels']) == 2  # testuser2 is only in 2 channels

    # Check for expected channel names
    channel_names = [channel['name'] for channel in data['channels']]
    assert 'Test Channel 1' not in channel_names
    assert 'Test Channel 2' in channel_names
    assert 'DM: testuser1 & testuser2' in channel_names


def test_create_channel(logged_in_user1):
    """Test creating a new channel."""
    response = logged_in_user1.post(
        '/api/channels',
        json={
            'name': 'New Test Channel',
            'description': 'A new channel created in testing'
        },
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Channel created successfully'
    assert 'channel' in data
    assert data['channel']['name'] == 'New Test Channel'
    assert data['channel']['description'] == 'A new channel created in testing'


def test_create_direct_message_channel(logged_in_user1, app):
    """Test creating a direct message channel."""
    with app.app_context():
        # Get user_id for testuser2
        user2 = User.query.filter_by(username='testuser2').first()
        user2_id = user2.id

    response = logged_in_user1.post(
        '/api/channels',
        json={
            'name': 'DM: Test Direct Message',
            'is_direct': True,
            'member_ids': [user2_id]
        },
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'channel' in data
    assert data['channel']['is_direct'] == True


def test_get_channel(logged_in_user1):
    """Test getting a specific channel."""
    response = logged_in_user1.get('/api/channels/1')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'channel' in data
    assert data['channel']['id'] == 1
    assert data['channel']['name'] == 'Test Channel 1'
    assert 'members' in data
    assert len(data['members']) == 1  # Only testuser1 is a member


def test_get_channel_unauthorized(logged_in_user2):
    """Test getting a channel the user isn't a member of."""
    response = logged_in_user2.get('/api/channels/1')

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'You are not a member of this channel'


def test_update_channel(logged_in_user1):
    """Test updating a channel."""
    response = logged_in_user1.put(
        '/api/channels/1',
        json={
            'name': 'Updated Channel Name',
            'description': 'Updated channel description'
        },
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Channel updated successfully'
    assert 'channel' in data
    assert data['channel']['name'] == 'Updated Channel Name'
    assert data['channel']['description'] == 'Updated channel description'


def test_update_channel_unauthorized(logged_in_user2, app):
    """Test updating a channel as a non-owner."""
    with app.app_context():
        # Make sure testuser2 is a member of channel 2 but not the owner
        channel = Channel.query.get(2)
        assert channel.owner_id != 2

        # Get user_id for testuser2
        user2 = User.query.filter_by(username='testuser2').first()
        assert user2 in channel.members

    response = logged_in_user2.put(
        '/api/channels/2',
        json={
            'name': 'Unauthorized Update',
            'description': 'This should fail'
        },
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Only the channel owner can update the channel'


def test_delete_channel(logged_in_user1):
    """Test deleting a channel."""
    # Create a channel to delete
    create_response = logged_in_user1.post(
        '/api/channels',
        json={
            'name': 'Channel to Delete',
            'description': 'This channel will be deleted'
        },
        headers={'Content-Type': 'application/json'}
    )

    channel_id = json.loads(create_response.data)['channel']['id']

    # Delete the channel
    response = logged_in_user1.delete(f'/api/channels/{channel_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Channel deleted successfully'

    # Try to access the deleted channel
    response = logged_in_user1.get(f'/api/channels/{channel_id}')
    assert response.status_code == 404


def test_delete_channel_unauthorized(logged_in_user2):
    """Test deleting a channel as a non-owner."""
    response = logged_in_user2.delete('/api/channels/2')

    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Only the channel owner can delete the channel'


def test_add_member(logged_in_user1, app):
    """Test adding a member to a channel."""
    with app.app_context():
        # Create a new channel for testing
        new_channel = Channel(
            name='Member Test Channel',
            description='Testing adding members',
            owner_id=1
        )
        user1 = User.query.get(1)
        new_channel.members.append(user1)
        db = app.extensions['sqlalchemy'].db
        db.session.add(new_channel)
        db.session.commit()
        channel_id = new_channel.id

    # Add testuser2 to the channel
    response = logged_in_user1.post(
        f'/api/channels/{channel_id}/members',
        json={'user_id': 2},
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Member added successfully'

    # Verify member was added
    response = logged_in_user1.get(f'/api/channels/{channel_id}')
    data = json.loads(response.data)
    member_ids = [member['id'] for member in data['members']]
    assert 2 in member_ids


def test_remove_member(logged_in_user1, app):
    """Test removing a member from a channel."""
    with app.app_context():
        # Use channel 2 which has both users as members
        channel_id = 2
        user2_id = 2

    # Remove testuser2 from the channel
    response = logged_in_user1.delete(
        f'/api/channels/{channel_id}/members/{user2_id}'
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Member removed successfully'

    # Verify member was removed
    response = logged_in_user1.get(f'/api/channels/{channel_id}')
    data = json.loads(response.data)
    member_ids = [member['id'] for member in data['members']]
    assert 2 not in member_ids


def test_channel_web_views(logged_in_user1):
    """Test the web views for channels."""
    # Test channels index view
    response = logged_in_user1.get('/channels')
    assert response.status_code == 200
    assert b'Channels' in response.data

    # Test single channel view
    response = logged_in_user1.get('/channels/1')
    assert response.status_code == 200
    assert b'Test Channel 1' in response.data


def test_unauthorized_channel_view(logged_in_user2):
    """Test accessing a channel view the user isn't a member of."""
    response = logged_in_user2.get('/channels/1', follow_redirects=True)
    assert b'You are not a member of this channel' in response.data