import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Channel, Message


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True

    # Create the database and the tables
    with app.app_context():
        db.create_all()

        # Create test users
        test_user1 = User(
            username='testuser1',
            email='test1@example.com',
            password='password1',
            status='online'
        )
        test_user2 = User(
            username='testuser2',
            email='test2@example.com',
            password='password2',
            status='offline'
        )
        db.session.add(test_user1)
        db.session.add(test_user2)

        # Create test channels
        test_channel1 = Channel(
            name='Test Channel 1',
            description='Channel for testing',
            owner_id=1
        )
        test_channel1.members.append(test_user1)

        test_channel2 = Channel(
            name='Test Channel 2',
            description='Another channel for testing',
            owner_id=1
        )
        test_channel2.members.append(test_user1)
        test_channel2.members.append(test_user2)

        # Create direct message channel
        dm_channel = Channel(
            name='DM: testuser1 & testuser2',
            description='Direct Messages',
            is_direct=True,
            owner_id=1
        )
        dm_channel.members.append(test_user1)
        dm_channel.members.append(test_user2)

        db.session.add(test_channel1)
        db.session.add(test_channel2)
        db.session.add(dm_channel)

        # Create test messages
        test_message1 = Message(
            content='Test message 1 in channel 1',
            user_id=1,
            channel_id=1
        )
        test_message2 = Message(
            content='Test message 2 in channel 2',
            user_id=1,
            channel_id=2
        )
        test_message3 = Message(
            content='Test message from user 2 in channel 2',
            user_id=2,
            channel_id=2
        )
        test_dm_message = Message(
            content='Direct message from user 1 to user 2',
            user_id=1,
            channel_id=3
        )

        db.session.add(test_message1)
        db.session.add(test_message2)
        db.session.add(test_message3)
        db.session.add(test_dm_message)

        db.session.commit()

    yield app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def auth1(client):
    """Authentication helper for testuser1."""

    class AuthActions:
        def login(self, username='testuser1', password='password1'):
            return client.post(
                '/login',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )

        def logout(self):
            return client.get('/logout', headers={'Accept': 'application/json'})

    return AuthActions()


@pytest.fixture
def auth2(client):
    """Authentication helper for testuser2."""

    class AuthActions:
        def login(self, username='testuser2', password='password2'):
            return client.post(
                '/login',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )

        def logout(self):
            return client.get('/logout', headers={'Accept': 'application/json'})

    return AuthActions()


@pytest.fixture
def logged_in_user1(client, auth1):
    """Fixture to have testuser1 logged in."""
    auth1.login()
    return client


@pytest.fixture
def logged_in_user2(client, auth2):
    """Fixture to have testuser2 logged in."""
    auth2.login()
    return client