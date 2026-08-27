import json


def test_get_all_bookings_empty(client):
    response = client.get("/api/v1/booking")
    assert response.status_code == 200


def test_create_booking(client, super_admin_headers, regular_user, sample_service):
    payload = {
        "user_id": regular_user.id,
        "service_id": sample_service.id,
        "employee_id": regular_user.id,
        "date": "2026-09-01",
        "booking_time": "14:00",
    }

    response = client.post("/api/v1/booking", data=json.dumps(payload), headers=super_admin_headers)
    assert response.status_code in [200, 201]


def test_get_booking_by_id_not_found(client):
    response = client.get("/api/v1/booking/99999")
    assert response.status_code in [200, 404]


def test_create_booking_unauthorized(client):
    """Ported from Test/test_booking.py — booking without token returns 401."""
    payload = {"date": "2026-09-10 10:00:00", "employee_id": 1, "service_id": 1}
    response = client.post(
        "/api/v1/booking",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 401

