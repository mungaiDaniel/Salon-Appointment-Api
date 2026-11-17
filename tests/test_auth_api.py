import pytest
from passlib.hash import md5_crypt

from app.auth.model import User
from app.database.database import db
from tests.conftest import PASSWORD, login

VALID = {
    "firstName": "Alice",
    "lastName": "Smith",
    "email": "Alice@Example.com",
    "password": "Password123!",
    "location": "Nairobi",
    "phoneNumber": "+254 712 345678",
}


# ---------- registration ----------
def test_register_success_normalises_email_and_hides_password(client):
    response = client.post("/api/v1/users", json=VALID)
    assert response.status_code == 201
    body = response.get_json()
    assert body["email"] == "alice@example.com"
    assert body["user_role"] == "user"
    assert "password" not in body


def test_register_cannot_choose_own_role(client):
    response = client.post("/api/v1/users", json={**VALID, "user_role": "super_admin"})
    assert response.status_code == 201
    assert response.get_json()["user_role"] == "user"


def test_register_stores_modern_hash(client):
    client.post("/api/v1/users", json=VALID)
    stored = db.session.execute(db.select(User)).scalar_one().password
    assert stored.startswith(("scrypt:", "pbkdf2:"))


def test_register_duplicate_email_is_409(client, regular_user):
    response = client.post("/api/v1/users", json={**VALID, "email": regular_user.email})
    assert response.status_code == 409
    assert response.get_json()["code"] == "email_taken"


@pytest.mark.parametrize(
    "patch,field",
    [
        ({"email": "not-an-email"}, "email"),
        ({"password": "short"}, "password"),
        ({"phoneNumber": "abc"}, "phoneNumber"),
        ({"firstName": ""}, "firstName"),
    ],
)
def test_register_validation_errors_are_422(client, patch, field):
    response = client.post("/api/v1/users", json={**VALID, **patch})
    assert response.status_code == 422
    body = response.get_json()
    assert body["code"] == "validation_error"
    assert field in body["details"]


def test_register_missing_body_is_422(client):
    assert client.post("/api/v1/users").status_code == 422


# ---------- login ----------
def test_login_success_shape(client, regular_user):
    response = client.post(
        "/api/v1/login", json={"email": regular_user.email, "password": PASSWORD}
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["message"] == "SUCCESS."
    value = body["value"]
    assert value["user_role"] == "user"
    assert value["user"] == "Jane"
    assert value["access_token"] and value["refresh_token"]


def test_login_is_case_insensitive_on_email(client, regular_user):
    response = client.post(
        "/api/v1/login", json={"email": regular_user.email.upper(), "password": PASSWORD}
    )
    assert response.status_code == 200


def test_login_wrong_password_and_unknown_user_look_identical(client, regular_user):
    wrong = client.post("/api/v1/login", json={"email": regular_user.email, "password": "nope"})
    unknown = client.post("/api/v1/login", json={"email": "ghost@example.com", "password": "x"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.get_json() == unknown.get_json()


def test_login_missing_fields_is_422(client):
    response = client.post("/api/v1/login", json={"email": "a@example.com"})
    assert response.status_code == 422
    assert "password" in response.get_json()["details"]


def test_legacy_md5_hash_is_upgraded_on_login(client, regular_user):
    regular_user.password = md5_crypt.hash(PASSWORD)
    db.session.commit()

    login(client, regular_user.email)

    db.session.refresh(regular_user)
    assert not regular_user.password.startswith("$1$")
    login(client, regular_user.email)  # still works with the new hash


def test_legacy_hash_wrong_password_is_rejected_and_not_rehashed(client, regular_user):
    legacy = md5_crypt.hash(PASSWORD)
    regular_user.password = legacy
    db.session.commit()

    response = client.post("/api/v1/login", json={"email": regular_user.email, "password": "bad"})
    assert response.status_code == 401
    db.session.refresh(regular_user)
    assert regular_user.password == legacy


# ---------- tokens ----------
def test_refresh_token_issues_new_access_token(client, regular_user):
    refresh = login(client, regular_user.email)["refresh_token"]
    response = client.post("/api/v1/refresh", headers={"Authorization": f"Bearer {refresh}"})
    assert response.status_code == 200
    assert response.get_json()["value"]["access_token"]


def test_access_token_cannot_be_used_as_refresh_token(client, user_headers):
    assert client.post("/api/v1/refresh", headers=user_headers).status_code == 401


def test_garbage_token_is_401_json(client):
    response = client.get("/api/v1/booking", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401
    assert response.get_json()["code"] in {"invalid_token", "unauthorized"}


def test_token_for_deleted_user_is_rejected(client, regular_user, user_headers):
    db.session.delete(regular_user)
    db.session.commit()
    response = client.get("/api/v1/booking", headers=user_headers)
    assert response.status_code == 401
    assert response.get_json()["code"] == "user_not_found"


# ---------- users & roles ----------
def test_list_users_requires_auth(client):
    assert client.get("/api/v1/users").status_code == 401


def test_list_users_forbidden_for_customer(client, user_headers):
    response = client.get("/api/v1/users", headers=user_headers)
    assert response.status_code == 403
    assert response.get_json()["code"] == "insufficient_role"


def test_list_users_for_admin_never_leaks_password_hash(client, admin_headers, regular_user):
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.get_json()
    assert {u["email"] for u in users} >= {regular_user.email, "admin@example.com"}
    assert all("password" not in u for u in users)


def test_user_can_read_own_profile_but_not_others(client, regular_user, other_user, user_headers):
    assert client.get(f"/api/v1/users/{regular_user.id}", headers=user_headers).status_code == 200
    assert client.get(f"/api/v1/users/{other_user.id}", headers=user_headers).status_code == 403


def test_admin_can_read_any_profile_and_missing_is_404(client, regular_user, admin_headers):
    assert client.get(f"/api/v1/users/{regular_user.id}", headers=admin_headers).status_code == 200
    missing = client.get("/api/v1/users/99999", headers=admin_headers)
    assert missing.status_code == 404
    assert missing.get_json()["code"] == "user_not_found"


def test_promote_requires_super_admin(client, regular_user, user_headers, admin_headers):
    url = f"/api/v1/admin/{regular_user.id}"
    assert client.put(url).status_code == 401
    assert client.put(url, headers=user_headers).status_code == 403
    assert client.put(url, headers=admin_headers).status_code == 403


def test_super_admin_can_promote_to_admin_and_super_admin(client, regular_user, super_headers):
    r1 = client.put(f"/api/v1/admin/{regular_user.id}", headers=super_headers)
    assert r1.status_code == 200 and r1.get_json()["user_role"] == "admin"
    r2 = client.put(f"/api/v1/super_admin/{regular_user.id}", headers=super_headers)
    assert r2.status_code == 200 and r2.get_json()["user_role"] == "super_admin"


def test_promoted_user_gains_access_immediately(client, regular_user, user_headers, super_headers):
    assert client.get("/api/v1/users", headers=user_headers).status_code == 403
    client.put(f"/api/v1/admin/{regular_user.id}", headers=super_headers)
    assert client.get("/api/v1/users", headers=user_headers).status_code == 200  # same token


def test_promote_missing_user_is_404(client, super_headers):
    assert client.put("/api/v1/admin/99999", headers=super_headers).status_code == 404


def test_employees_public_list_hides_contact_details(client, admin_user):
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    staff = response.get_json()
    assert [s["firstName"] for s in staff] == ["Admin"]
    assert "email" not in staff[0] and "phoneNumber" not in staff[0]


def test_employees_list_includes_contact_details_for_admins(client, admin_user, admin_headers):
    staff = client.get("/api/v1/employees", headers=admin_headers).get_json()
    assert staff[0]["email"] == "admin@example.com"


def test_employees_excludes_customers(client, regular_user, admin_user):
    emails = [s.get("firstName") for s in client.get("/api/v1/employees").get_json()]
    assert "Jane" not in emails
