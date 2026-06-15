import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Create a test client — this simulates HTTP requests without running a server
client = TestClient(app)

# ■■ Health Endpoint Tests ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
def test_health_returns_200():
    """Health endpoint must return HTTP 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200

def test_health_returns_healthy_status():
    """Health endpoint must return status: healthy"""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"

def test_health_has_timestamp():
    """Health endpoint must include a timestamp"""
    response = client.get("/health")
    data = response.json()
    assert "timestamp" in data

# ■■ Info Endpoint Tests ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
def test_info_returns_200():
    """Info endpoint must return HTTP 200 OK"""
    response = client.get("/info")
    assert response.status_code == 200

def test_info_has_required_fields():
    """Info endpoint must return project, version, and author"""
    response = client.get("/info")
    data = response.json()
    assert "project" in data
    assert "version" in data
    assert "author" in data

def test_info_correct_project_name():
    """Info endpoint must return correct project name"""
    response = client.get("/info")
    data = response.json()
    assert data["project"] == "AutoDeploy"

# ■■ Predict Endpoint Tests ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
def test_predict_returns_200():
    """Predict endpoint must return HTTP 200 for valid input"""
    response = client.post("/predict", json={"text": "This is a great product!"})
    assert response.status_code == 200

def test_predict_positive_sentiment():
    """Predict endpoint should return positive for clearly positive text"""
    response = client.post("/predict", json={"text": "I love this amazing product"})
    data = response.json()
    assert data["sentiment"] == "positive"

def test_predict_negative_sentiment():
    """Predict endpoint should return negative for clearly negative text"""
    response = client.post("/predict", json={"text": "This is terrible and awful"})
    data = response.json()
    assert data["sentiment"] == "negative"

def test_predict_returns_word_count():
    """Predict endpoint must return correct word count"""
    response = client.post("/predict", json={"text": "one two three"})
    data = response.json()
    assert data["word_count"] == 3

def test_predict_empty_text_returns_400():
    """Predict endpoint must reject empty text with 400 error"""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 400

def test_predict_has_confidence_score():
    """Predict endpoint must return a confidence score between 0 and 1"""
    response = client.post("/predict", json={"text": "This is good"})
    data = response.json()
    assert 0.0 <= data["confidence"] <= 1.0
