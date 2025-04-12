import json
import pytest
from flask import session


def test_register(client):
    """Test user registration."""
    # Test form submission
    response = client.post(
        '/register',
        data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        },
        follow_redirects=True
    )
    assert b'Login' in response.data

    # Test API registration
    response = client.post(
        '/register',
        json={
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'apipassword'
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'User registered successfully'


def test_register_validation(client):
    """Test registration validation."""
    # Test duplicate username
    response = client.post(
        '/register',
        json={
            'username': 'testuser1',  # Already exists
            'email': 'unique@example.com',
            'password': 'password'
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Username already exists' in data['error']

    # Test duplicate email
    response = client.post(
        '/register',
        json={
            'username': 'uniqueuser',
            'email': 'test1@example.com',  # Already exists
            'password': 'password'
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Email already exists' in data['error']


def test_login(client, auth1):
    """Test user login."""
    # Test form submission
    response = client.post(
        '/login',
        data={
            'username': 'testuser1',
            'password': 'password1'
        },
        follow_redirects=True
    )
    assert b'Welcome to Flask Chat' in response.data

    # Test API login
    response = auth1.login()
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Login successful'
    assert 'user' in data
    assert data['user']['username'] == 'testuser1'


def test_login_validation(client):
    """Test login validation."""
    # Test invalid username
    response = client.post(
        '/login',
        json={
            'username': 'nonexistent',
            'password': 'password'
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid username or password'

    # Test invalid password
    response = client.post(
        '/login',
        json={
            'username': 'testuser1',
            'password': 'wrongpassword'
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid username or password'


def test_logout(client, auth1):
    """Test user logout."""
    # Login first
    auth1.login()

    # Test API logout
    response = auth1.logout()
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Logout successful'

    # Test form logout with redirect
    auth1.login()
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data


def test_auth_required_redirect(client):
    """Test authentication-required redirect."""
    # Try accessing a protected route without login
    response = client.get('/channels', follow_redirects=True)
    assert b'Login' in response.data

    # Try accessing API without login
    response = client.get('/api/channels')
    assert response.status_code == 302  # Redirect to login


def test_authenticate_with_valid_credentials(client, auth1):
    """Test login flow and session."""
    auth1.login()

    # Access a protected route after login
    response = client.get('/channels')
    assert response.status_code == 200
    assert b'Channels' in response.data