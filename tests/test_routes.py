import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db
from api.models import User, Poll
from api.schemas import UserCreate, PollCreate
from main import app


# Use a separate test database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_polls.db"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drop tables and remove test db
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_polls.db"):
        os.remove("./test_polls.db")


client = TestClient(app)


def test_register():
    response = client.post(
        "/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login():
    response = client.post(
        "/login", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    global token
    token = data["access_token"]


def test_get_polls_empty():
    response = client.get("/polls")
    assert response.status_code == 200
    assert response.json() == []


def test_create_poll():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/polls", json={"question": "Is this a test poll?"}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Is this a test poll?"
    assert "id" in data
    global poll_id
    poll_id = data["id"]


def test_get_polls_with_data():
    response = client.get("/polls")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["question"] == "Is this a test poll?"


def test_delete_poll():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/polls/{poll_id}", headers=headers)
    assert response.status_code == 204


def test_get_polls_after_delete():
    response = client.get("/polls")
    assert response.status_code == 200
    assert response.json() == []
