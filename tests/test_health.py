import json


def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert data["db"] == "connected"


def test_api_v1_health_check_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert data["db"] == "connected"
