"""
Pytest Configuration and Fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "securepassword123",
        "is_active": True
    }


@pytest.fixture
def mock_user():
    """Mock user object"""
    from datetime import datetime
    from app.models.user import User
    
    return User(
        id=1,
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        is_active=True,
        created_at=datetime.now()
    )