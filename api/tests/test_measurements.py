import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

def test_analyze_measurements_base64(client, auth_headers, sample_measurement_request):
    """Test measurement analysis with base64 image"""
    response = client.post(
        "/api/v1/measurements/analyze-base64",
        json=sample_measurement_request,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "measurements" in data
    assert "processing_time" in data
    assert "model_version" in data
    assert "timestamp" in data
    
    # Check that all expected measurements are present
    measurements = data["measurements"]
    expected_keys = [
        "height", "waist", "belly", "chest", "wrist", "neck",
        "arm_length", "thigh", "shoulder_width", "hips", "ankle"
    ]
    for key in expected_keys:
        assert key in measurements
        assert isinstance(measurements[key], (int, float))

def test_analyze_measurements_file_upload(client, auth_headers):
    """Test measurement analysis with file upload"""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    response = client.post(
        "/api/v1/measurements/analyze",
        data={"height": 72.0},
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "measurements" in data

def test_analyze_measurements_invalid_height(client, auth_headers, sample_measurement_request):
    """Test measurement analysis with invalid height"""
    # Test negative height
    invalid_request = sample_measurement_request.copy()
    invalid_request["height"] = -10
    
    response = client.post(
        "/api/v1/measurements/analyze-base64",
        json=invalid_request,
        headers=auth_headers
    )
    
    assert response.status_code == 422  # Validation error

def test_analyze_measurements_unauthorized(client, sample_measurement_request):
    """Test measurement analysis without authentication"""
    response = client.post(
        "/api/v1/measurements/analyze-base64",
        json=sample_measurement_request
    )
    
    assert response.status_code == 401

def test_analyze_measurements_invalid_file_type(client, auth_headers):
    """Test measurement analysis with invalid file type"""
    # Create a text file instead of image
    text_file = io.BytesIO(b"This is not an image")
    
    response = client.post(
        "/api/v1/measurements/analyze",
        data={"height": 72.0},
        files={"image": ("test.txt", text_file, "text/plain")},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "File must be an image" in response.json()["error"]

def test_measurements_health_check(client):
    """Test measurements health check endpoint"""
    response = client.get("/api/v1/measurements/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "service" in data

def test_rate_limiting(client, auth_headers, sample_measurement_request):
    """Test rate limiting functionality"""
    # Make multiple requests quickly to trigger rate limiting
    for i in range(15):  # More than the rate limit
        response = client.post(
            "/api/v1/measurements/analyze-base64",
            json=sample_measurement_request,
            headers=auth_headers
        )
        
        if i < 10:  # First 10 should succeed
            assert response.status_code == 200
        else:  # After rate limit, should get 429
            assert response.status_code == 429

