import pytest

PAYLOAD = {"style": "Blowdry", "description": "Smooth finish", "cost": 34.5, "duration": 45}


def test_list_and_get_are_public(client, sample_service):
    listing = client.get("/api/v1/stylings")
    assert listing.status_code == 200 and len(listing.get_json()) == 1
    one = client.get(f"/api/v1/stylings/{sample_service.id}")
    assert one.status_code == 200 and one.get_json()["style"] == "Haircut & Styling"


def test_get_missing_service_is_404(client):
    response = client.get("/api/v1/stylings/99999")
    assert response.status_code == 404
    assert response.get_json()["code"] == "service_not_found"


def test_create_requires_token(client):
    assert client.post("/api/v1/stylings", json=PAYLOAD).status_code == 401


def test_create_forbidden_for_customer(client, user_headers):
    assert client.post("/api/v1/stylings", json=PAYLOAD, headers=user_headers).status_code == 403


@pytest.mark.parametrize("headers_fixture", ["admin_headers", "super_headers"])
def test_create_allowed_for_staff(client, request, headers_fixture):
    headers = request.getfixturevalue(headers_fixture)
    response = client.post("/api/v1/stylings", json=PAYLOAD, headers=headers)
    assert response.status_code == 201
    body = response.get_json()
    assert body["style"] == "Blowdry" and body["user_id"]


@pytest.mark.parametrize(
    "patch",
    [{"cost": -1}, {"duration": 0}, {"duration": "soon"}, {"style": ""}, {"cost": "free"}],
)
def test_create_validation_errors_are_422(client, admin_headers, patch):
    response = client.post("/api/v1/stylings", json={**PAYLOAD, **patch}, headers=admin_headers)
    assert response.status_code == 422


def test_create_missing_fields_is_422(client, admin_headers):
    response = client.post("/api/v1/stylings", json={"style": "x"}, headers=admin_headers)
    assert response.status_code == 422
    assert set(response.get_json()["details"]) == {"cost", "duration"}


def test_update_service(client, sample_service, admin_headers):
    response = client.put(
        f"/api/v1/stylings/{sample_service.id}", json=PAYLOAD, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.get_json()["cost"] == 34.5


def test_update_missing_keys_is_422_not_500(client, sample_service, admin_headers):
    response = client.put(
        f"/api/v1/stylings/{sample_service.id}", json={"style": "x"}, headers=admin_headers
    )
    assert response.status_code == 422


def test_update_is_protected(client, sample_service, user_headers):
    url = f"/api/v1/stylings/{sample_service.id}"
    assert client.put(url, json=PAYLOAD).status_code == 401
    assert client.put(url, json=PAYLOAD, headers=user_headers).status_code == 403


def test_update_missing_service_is_404(client, admin_headers):
    assert (
        client.put("/api/v1/stylings/99999", json=PAYLOAD, headers=admin_headers).status_code == 404
    )


def test_delete_service(client, sample_service, admin_headers):
    url = f"/api/v1/stylings/{sample_service.id}"
    assert client.delete(url, headers=admin_headers).status_code == 200
    assert client.get(url).status_code == 404


def test_delete_is_protected(client, sample_service, user_headers):
    url = f"/api/v1/stylings/{sample_service.id}"
    assert client.delete(url).status_code == 401
    assert client.delete(url, headers=user_headers).status_code == 403


def test_delete_missing_service_is_404(client, admin_headers):
    assert client.delete("/api/v1/stylings/99999", headers=admin_headers).status_code == 404
