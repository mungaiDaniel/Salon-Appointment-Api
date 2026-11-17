def test_assign_requires_admin(client, regular_user, sample_service, user_headers):
    url = f"/api/v1/employee/{regular_user.id}/{sample_service.id}"
    assert client.post(url).status_code == 401
    assert client.post(url, headers=user_headers).status_code == 403


def test_assign_and_list_employee_services(client, admin_user, sample_service, admin_headers):
    response = client.post(
        f"/api/v1/employee/{admin_user.id}/{sample_service.id}", headers=admin_headers
    )
    assert response.status_code == 201
    assert response.get_json()["service_id"] == sample_service.id

    links = client.get(f"/api/v1/employee/{admin_user.id}").get_json()
    assert [link["service_id"] for link in links] == [sample_service.id]

    services = client.get(f"/api/v1/employee_service/{admin_user.id}").get_json()
    assert [s["style"] for s in services] == ["Haircut & Styling"]


def test_assign_twice_is_409(client, admin_user, sample_service, admin_headers):
    url = f"/api/v1/employee/{admin_user.id}/{sample_service.id}"
    client.post(url, headers=admin_headers)
    assert client.post(url, headers=admin_headers).status_code == 409


def test_assign_unknown_user_or_service_is_404(client, admin_user, sample_service, admin_headers):
    assert (
        client.post(f"/api/v1/employee/999/{sample_service.id}", headers=admin_headers).status_code
        == 404
    )
    assert (
        client.post(f"/api/v1/employee/{admin_user.id}/999", headers=admin_headers).status_code
        == 404
    )


def test_unknown_employee_has_no_services(client):
    assert client.get("/api/v1/employee/99999").get_json() == []
    assert client.get("/api/v1/employee_service/99999").get_json() == []
