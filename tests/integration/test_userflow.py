"""
Integration tests for user authentication endpoints in the Flask application,
including tests for the following functionality:
- Successful registration and login
- Duplicate registration attempts
- Login attempts for non-existent users

It uses a test client and an in-memory database setup via pytest fixtures.
"""

import pytest

from app import app, db


@pytest.fixture(scope="module")
def test_client():
    """
    Provides a Flask test client with an in-memory database.
    This fixture initializes the database schema before tests run
    and cleans it up afterward.
    """
    
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client

    db.drop_all()
    ctx.pop()

def test_register_user(test_client):
    """
    Tests user registration.
    Verifies that the response contains a new user_id and the correct username.
    """
    
    response = test_client.post("/register", json={"username": "alice"})
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "alice"

def test_login_user(test_client):
    """
    Tests user login.
    Verifies that the response returns the expected user_id and username.
    """
    
    response = test_client.post("/login", json={"username": "alice"})
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "alice"

def test_register_existing_user(test_client):
    """
    Tests the registration of an existing user.
    Verifies that the registration of an existing user raises an error.
    """
    
    response = test_client.post("/register", json={"username": "alice"})
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "User already exists"

def test_login_nonexistent_user(test_client):
    """
    Tests login attempt for a user that does not exist.
    Verifies that trying to login with a nonexistent user raises an error.
    """
    
    response = test_client.post("/login", json={"username": "bob"})
    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "User does not exist"
