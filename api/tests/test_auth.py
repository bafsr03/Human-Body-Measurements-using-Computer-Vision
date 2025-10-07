import pytest
from fastapi.testclient import TestClient

def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["username"] == "newuser"

def test_register_existing_user(client):
    """Test registration with existing username"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    # First registration
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Second registration with same username
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["error"]

def test_login_success(client):
    """Test successful login"""
    # First register a user
    user_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "logintestpass"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "username": "logintest",
        "password": "logintestpass"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["error"]

def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

