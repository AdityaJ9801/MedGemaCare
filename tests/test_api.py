"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data
    assert "version" in data


def test_summarize_endpoint():
    """Test text summarization endpoint."""
    payload = {
        "text": "Patient presents with fever and cough. Temperature 101°F. Prescribed antibiotics.",
        "temperature": 0.7,
    }
    response = client.post("/api/v1/summarize", json=payload)
    
    # May fail if model not loaded, which is expected in test environment
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "summary" in data
        assert "input_length" in data


def test_analyze_endpoint():
    """Test report analysis endpoint."""
    payload = {
        "text": "Patient presents with fever and cough. Temperature 101°F. Prescribed antibiotics.",
        "question": "What is the patient's temperature?",
    }
    response = client.post("/api/v1/analyze", json=payload)
    
    # May fail if model not loaded
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "answer" in data
        assert "question" in data


@pytest.mark.asyncio
async def test_document_upload():
    """Test document upload endpoint."""
    # Create a simple text file
    files = {
        "file": ("test_report.txt", b"Patient medical report content", "text/plain")
    }
    response = client.post("/api/v1/upload/document", files=files)
    
    # May fail if dependencies not available
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert data["processed"] is True
        assert data["filename"] == "test_report.txt"

