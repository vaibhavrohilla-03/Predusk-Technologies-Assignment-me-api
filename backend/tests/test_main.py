from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_top_skills_unseeded():
    response = client.get("/skills/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_endpoint():
    response = client.get("/search?q=python")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert "skills" in data