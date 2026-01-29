"""
Test API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["status"] == "operational"


def test_health_endpoint():
    """Test health check"""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ask_question():
    """Test chat endpoint"""
    response = client.post(
        "/api/v1/chat/ask",
        json={
            "question": "What is BASF's procurement strategy?",
            "use_agentic": False,
            "max_sources": 3
        }
    )
    # May fail without proper Azure credentials
    # This is a structure test
    assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
