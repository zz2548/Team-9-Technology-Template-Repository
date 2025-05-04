"""
Integration tests for user-related API endpoints.

These tests cover user registration, login, and error cases for both operations.
They simulate client requests to the Flask application using a test client and
an in-memory database.
"""

import pytest
from app import app, db

@pytest.fixture(scope="module")
def test_client() -> None:
    """
    Provides a Flask test client with application context and in-memory database.

    This fixture sets up a temporary test environment for the Flask app, including
    pushing the app context and creating the in-memory database tables before
    yielding the test client. After the tests finish, it tears down the context and drops the database.
    """
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client

    db.drop_all()
    ctx.pop()

def test_register_user(test_client) -> None:
    """
    Tests user registration endpoint.

    Verifies that a user can be registered with a username and password
    and that the response includes the expected user data.
    """
    response = test_client.post("/register", json={
        "username": "alice",
        "password": "securepassword"
    })
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "alice"
    assert "token" in data

def test_login_user(test_client) -> None:
    """
    Tests user login endpoint.

    Verifies that a registered user can log in with correct credentials
    and that the response includes the expected user data.
    """
    # Register a user first
    test_client.post("/register", json={
        "username": "bob",
        "password": "password123"
    })

    # Then try to log in
    response = test_client.post("/login", json={
        "username": "bob",
        "password": "password123"
    })
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "bob"
    assert "token" in data

def test_register_existing_user(test_client) -> None:
    """
    Tests registration attempt for a user that already exists.

    Verifies that trying to register with an existing username raises an error.
    """
    # Register a user
    test_client.post("/register", json={
        "username": "charlie",
        "password": "password456"
    })

    # Try to register the same user again
    response = test_client.post("/register", json={
        "username": "charlie",
        "password": "differentpassword"
    })
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "User already exists"

def test_login_nonexistent_user(test_client) -> None:
    """
    Tests login attempt for a user that does not exist.

    Verifies that trying to login with a nonexistent user raises an error.
    """
    response = test_client.post("/login", json={
        "username": "nonexistent",
        "password": "anypassword"
    })
    assert response.status_code == 401

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid username or password"

def test_login_wrong_password(test_client) -> None:
    """
    Tests login attempt with incorrect password.

    Verifies that trying to login with the wrong password raises an error.
    """
    # Register a user
    test_client.post("/register", json={
        "username": "dave",
        "password": "correctpassword"
    })

    # Try to log in with wrong password
    response = test_client.post("/login", json={
        "username": "dave",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid username or password"

def test_missing_credentials(test_client) -> None:
    """
    Tests login and registration attempts with missing credentials.

    Verifies that requests without username or password are rejected.
    """
    # Test registration with missing password
    response = test_client.post("/register", json={"username": "incomplete"})
    assert response.status_code == 400

    # Test login with missing username
    response = test_client.post("/login", json={"password": "incomplete"})
    assert response.status_code == 400