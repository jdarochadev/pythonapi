import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.modules.users.schemas import UserCreate
from app.modules.users.repository import create_user

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    return user_data

@pytest.fixture
def test_token(client, test_user):
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]

@pytest.fixture
def authenticated_client(client, test_token):
    client.headers = {"Authorization": f"Bearer {test_token}"}
    return client
