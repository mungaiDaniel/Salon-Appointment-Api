import json


def test_user_registration_success(client):
    payload = {
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice@example.com",
        "password": "Password123!",
        "location": "Nairobi",
        "phoneNumber": "0712345678",
    }
    response = client.post(
        "/api/v1/users", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["email"] == "alice@example.com"
    assert data["firstName"] == "Alice"


def test_user_registration_duplicate_email(client, regular_user):
    payload = {
        "firstName": "Duplicate",
        "lastName": "User",
        "email": regular_user.email,
        "password": "Password123!",
        "location": "Nairobi",
        "phoneNumber": "0712345678",
    }
    response = client.post(
        "/api/v1/users", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 409


def test_login_invalid_password(client, regular_user):
    payload = {"email": regular_user.email, "password": "WrongPassword!"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert (
        response.status_code == 400
        or response.status_code == 401
        or response.status_code == 999
        or response.status_code == 404
    )


def test_login_missing_fields(client):
    payload = {"email": "missing.password@example.com"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code != 200


def test_promote_user_to_admin(client, regular_user):
    response = client.put(f"/api/v1/admin/{regular_user.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["user_role"] == "admin"


def test_promote_user_to_super_admin(client, regular_user):
    response = client.put(f"/api/v1/super_admin/{regular_user.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["user_role"] == "super_admin"


def test_get_all_employees(client, super_admin_user):
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_login_success_response_shape(client, super_admin_user):
    """Ported from Test/test_user.py — verifies login returns access_token and SUCCESS message."""
    payload = {"email": "superadmin@salon.com", "password": "Admin123!"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "access_token" in data.get("value", {})
    assert data.get("message") == "SUCCESS."


def test_get_nonexistent_user_404(client):
    """Ported from Test/test_user.py — nonexistent user returns 404."""
    response = client.get("/api/v1/users/99999", content_type="application/json")
    assert response.status_code == 404


def test_promote_nonexistent_user_404(client):
    """Ported from Test/test_user.py — promoting nonexistent user returns 404."""
    response = client.put("/api/v1/super_admin/99999", content_type="application/json")
    assert response.status_code == 404


def test_user_not_found_login(client):
    """Ported from Test/test_user.py — login with unregistered email returns 404."""
    payload = {"email": "nobody@example.com", "password": "password"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 404


def test_login_as_super_admin_returns_expected_shape(client, super_admin_user):
    """Verify refactored login returns correct shape for super_admin role."""
    payload = {"email": "superadmin@salon.com", "password": "Admin123!"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    value = data["value"]
    assert "access_token" in value
    assert "refresh_token" in value
    assert value["user_role"] == "super_admin"
    assert value["user"] == "Super"


def test_login_as_admin_returns_expected_shape(client, admin_user):
    """Verify refactored login returns correct shape for admin role."""
    payload = {"email": "admin@salon.com", "password": "Admin123!"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    value = data["value"]
    assert "access_token" in value
    assert "refresh_token" in value
    assert value["user_role"] == "admin"
    assert value["user"] == "Admin"


def test_login_as_regular_user_returns_expected_shape(client, regular_user):
    """Verify refactored login returns correct shape for user role."""
    payload = {"email": "jane.doe@salon.com", "password": "User123!"}
    response = client.post(
        "/api/v1/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    value = data["value"]
    assert "access_token" in value
    assert "refresh_token" in value
    assert value["user_role"] == "user"
    assert value["user"] == "Jane"
