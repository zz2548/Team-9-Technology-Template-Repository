import pytest

from app import app, db


@pytest.fixture(scope="module")
def test_client():
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client

    db.drop_all()
    ctx.pop()

def test_register_user(test_client):
    response = test_client.post("/register", json={"username": "alice"})
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "alice"

def test_login_user(test_client):
    response = test_client.post("/login", json={"username": "alice"})
    assert response.status_code == 200

    data = response.get_json()
    assert "user_id" in data
    assert data["username"] == "alice"

def test_register_existing_user(test_client):
    response = test_client.post("/register", json={"username": "alice"})
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "User already exists"

def test_login_nonexistent_user(test_client):
    response = test_client.post("/login", json={"username": "bob"})
    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "User does not exist"
