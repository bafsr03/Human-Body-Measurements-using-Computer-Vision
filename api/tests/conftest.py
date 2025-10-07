import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.redis_client import redis_client

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

@pytest.fixture
async def auth_headers(client):
    """Get authentication headers for testing"""
    # Register a test user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_image_base64():
    """Sample base64 encoded image for testing"""
    # This is a minimal 1x1 pixel PNG image in base64
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

@pytest.fixture
def sample_measurement_request():
    """Sample measurement request data"""
    return {
        "height": 72.0,
        "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    }

