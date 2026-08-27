import json


def test_add_employee_assistance(client, regular_user, sample_service):
    response = client.post(f"/api/v1/employee/{regular_user.id}/{sample_service.id}")
    assert response.status_code in [200, 201]


def test_get_employee_assistance(client, regular_user):
    response = client.get(f"/api/v1/employee/{regular_user.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_employee_assistance_nonexistent_user(client):
    """Ported from Test/test_assistance.py — nonexistent user returns empty list."""
    response = client.get("/api/v1/employee/99999", content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

