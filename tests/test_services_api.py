import json


def test_create_service_authorized(client, super_admin_headers):
    """Super-admin can create a new styling service."""
    payload = {
        "style": "Blowdry",
        "description": (
            "Straightening is the art of blow drying"
            " your hair with hot iron to straighten it"
        ),
        "cost": 34.50,
        "duration": 2,
    }
    response = client.post(
        "/api/v1/stylings",
        data=json.dumps(payload),
        headers=super_admin_headers,
    )
    assert response.status_code in [200, 201]
    data = json.loads(response.data)
    assert data["style"] == "Blowdry"


def test_create_service_unauthorized(client):
    """Creating a service without a token returns 401."""
    payload = {
        "style": "Blowdry",
        "description": "Blow drying hair",
        "cost": 34.50,
        "duration": 2,
    }
    response = client.post(
        "/api/v1/stylings",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 401


def test_get_all_services(client):
    """Listing all services returns 200 even when empty."""
    response = client.get("/api/v1/stylings", content_type="application/json")
    assert response.status_code == 200


def test_get_one_service(client, super_admin_headers):
    """Fetching a service by ID after creation returns 200."""
    payload = {
        "style": "Blowdry",
        "description": "Blow drying hair with hot iron",
        "cost": 34.50,
        "duration": 2,
    }
    client.post(
        "/api/v1/stylings",
        data=json.dumps(payload),
        headers=super_admin_headers,
    )
    response = client.get("/api/v1/stylings/1", content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["style"] == "Blowdry"


def test_get_nonexistent_service(client):
    """Fetching a service that doesn't exist returns 404."""
    response = client.get("/api/v1/stylings/99999", content_type="application/json")
    assert response.status_code == 404


def test_update_service(client, super_admin_headers):
    """Updating an existing service returns 200 with updated data."""
    create_payload = {
        "style": "Blowdry",
        "description": "Blow drying hair",
        "cost": 34.50,
        "duration": 2,
    }
    client.post(
        "/api/v1/stylings",
        data=json.dumps(create_payload),
        headers=super_admin_headers,
    )
    update_payload = {
        "style": "Treatment",
        "description": "Deep conditioning treatment",
        "cost": 1000.50,
        "duration": 3,
    }
    response = client.put(
        "/api/v1/stylings/1",
        data=json.dumps(update_payload),
        headers=super_admin_headers,
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["style"] == "Treatment"
    assert data["cost"] == 1000.50


def test_update_nonexistent_service(client, super_admin_headers):
    """Updating a nonexistent service returns 404."""
    update_payload = {
        "style": "Treatment",
        "description": "Treatment description",
        "cost": 100.0,
        "duration": 1,
    }
    response = client.put(
        "/api/v1/stylings/99999",
        data=json.dumps(update_payload),
        headers=super_admin_headers,
    )
    assert response.status_code == 404


def test_delete_nonexistent_service(client, super_admin_headers):
    """Deleting a nonexistent service returns 404."""
    response = client.delete(
        "/api/v1/stylings/99999",
        headers=super_admin_headers,
    )
    assert response.status_code == 404
