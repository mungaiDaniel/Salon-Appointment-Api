def booking(service, employee=None, date="2030-09-01T14:00:00"):
    body = {"service_id": service.id, "date": date}
    if employee is not None:
        body["employee_id"] = employee.id
    return body


def test_create_booking_requires_token(client, sample_service):
    assert client.post("/api/v1/booking", json=booking(sample_service)).status_code == 401


def test_create_booking_success_uses_token_identity(
    client, regular_user, admin_user, sample_service, user_headers
):
    response = client.post(
        "/api/v1/booking", json=booking(sample_service, admin_user), headers=user_headers
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["user_id"] == regular_user.id  # taken from the JWT, not the request body
    assert body["employee_id"] == admin_user.id
    assert body["date"].startswith("2030-09-01T14:00")


def test_client_cannot_book_on_behalf_of_someone_else(
    client, regular_user, other_user, sample_service, user_headers
):
    payload = {**booking(sample_service), "user_id": other_user.id}
    body = client.post("/api/v1/booking", json=payload, headers=user_headers).get_json()
    assert body["user_id"] == regular_user.id


def test_date_only_and_space_separated_formats_are_accepted(client, sample_service, user_headers):
    for date in ("2030-09-02", "2030-09-03 10:30:00"):
        response = client.post(
            "/api/v1/booking", json=booking(sample_service, date=date), headers=user_headers
        )
        assert response.status_code == 201, date


def test_timezone_aware_dates_are_stored_as_utc(client, sample_service, user_headers):
    response = client.post(
        "/api/v1/booking",
        json=booking(sample_service, date="2030-09-01T14:00:00+03:00"),
        headers=user_headers,
    )
    assert response.get_json()["date"].startswith("2030-09-01T11:00")


def test_invalid_date_is_422(client, sample_service, user_headers):
    response = client.post(
        "/api/v1/booking", json=booking(sample_service, date="tomorrow"), headers=user_headers
    )
    assert response.status_code == 422
    assert "date" in response.get_json()["details"]


def test_missing_fields_is_422(client, user_headers):
    response = client.post("/api/v1/booking", json={}, headers=user_headers)
    assert response.status_code == 422
    assert set(response.get_json()["details"]) == {"date", "service_id"}


def test_unknown_service_is_404(client, user_headers):
    response = client.post(
        "/api/v1/booking", json={"service_id": 999, "date": "2030-01-01"}, headers=user_headers
    )
    assert response.status_code == 404
    assert response.get_json()["code"] == "service_not_found"


def test_unknown_employee_is_404(client, sample_service, user_headers):
    payload = {**booking(sample_service), "employee_id": 999}
    response = client.post("/api/v1/booking", json=payload, headers=user_headers)
    assert response.status_code == 404
    assert response.get_json()["code"] == "employee_not_found"


def test_double_booking_same_employee_and_slot_is_409(
    client, admin_user, sample_service, user_headers, other_headers
):
    payload = booking(sample_service, admin_user)
    assert client.post("/api/v1/booking", json=payload, headers=user_headers).status_code == 201
    second = client.post("/api/v1/booking", json=payload, headers=other_headers)
    assert second.status_code == 409
    assert second.get_json()["code"] == "slot_unavailable"


def test_same_slot_with_different_employee_is_fine(
    client, admin_user, super_admin_user, sample_service, user_headers, other_headers
):
    one = client.post(
        "/api/v1/booking", json=booking(sample_service, admin_user), headers=user_headers
    )
    two = client.post(
        "/api/v1/booking", json=booking(sample_service, super_admin_user), headers=other_headers
    )
    assert one.status_code == two.status_code == 201


def test_list_requires_token(client):
    assert client.get("/api/v1/booking").status_code == 401


def test_customer_sees_only_own_bookings_admin_sees_all(
    client, admin_user, sample_service, user_headers, other_headers, admin_headers
):
    client.post(
        "/api/v1/booking", json=booking(sample_service, date="2030-01-01"), headers=user_headers
    )
    client.post(
        "/api/v1/booking", json=booking(sample_service, date="2030-01-02"), headers=other_headers
    )

    assert len(client.get("/api/v1/booking", headers=user_headers).get_json()) == 1
    assert len(client.get("/api/v1/booking", headers=other_headers).get_json()) == 1
    assert len(client.get("/api/v1/booking", headers=admin_headers).get_json()) == 2


def test_get_one_booking_owner_admin_and_stranger(
    client, sample_service, user_headers, other_headers, admin_headers
):
    created = client.post(
        "/api/v1/booking", json=booking(sample_service), headers=user_headers
    ).get_json()
    url = f"/api/v1/booking/{created['id']}"
    assert client.get(url, headers=user_headers).status_code == 200
    assert client.get(url, headers=admin_headers).status_code == 200
    assert client.get(url, headers=other_headers).status_code == 403
    assert client.get(url).status_code == 401


def test_get_missing_booking_is_404(client, user_headers):
    response = client.get("/api/v1/booking/99999", headers=user_headers)
    assert response.status_code == 404
    assert response.get_json()["code"] == "booking_not_found"
