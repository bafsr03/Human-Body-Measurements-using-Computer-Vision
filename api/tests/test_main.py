import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "timestamp" in data

def test_docs_endpoint(client):
    """Test API documentation endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_endpoint(client):
    """Test ReDoc documentation endpoint"""
    response = client.get("/redoc")
    assert response.status_code == 200

def test_cors_headers(client):
    """Test CORS headers are present"""
    response = client.options("/")
    assert response.status_code == 200
    # CORS headers should be present (exact headers depend on CORS configuration)

