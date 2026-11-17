import pytest
from werkzeug.security import generate_password_hash

from app.auth.model import User
from app.database.database import db
from app.service.model import Services
from config import TestingConfig
from main import create_app

PASSWORD = "Str0ngPass!"
# Production hashes use scrypt; a cheap PBKDF2 hash keeps the test suite fast.
_PASSWORD_HASH = generate_password_hash(PASSWORD, method="pbkdf2:sha256:1000")


@pytest.fixture()
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def _make_user(email, role, first="Test", phone="0711111111"):
    user = User(
        firstName=first,
        lastName="Person",
        email=email,
        password=_PASSWORD_HASH,
        location="Nairobi",
        user_role=role,
        phoneNumber=phone,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def regular_user(app):
    return _make_user("jane.doe@example.com", "user", "Jane")


@pytest.fixture()
def other_user(app):
    return _make_user("john.roe@example.com", "user", "John", "0722222222")


@pytest.fixture()
def admin_user(app):
    return _make_user("admin@example.com", "admin", "Admin", "0733333333")


@pytest.fixture()
def super_admin_user(app):
    return _make_user("super@example.com", "super_admin", "Super", "0744444444")


def login(client, email, password=PASSWORD):
    response = client.post("/api/v1/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.get_json()
    return response.get_json()["value"]


def bearer(client, email):
    return {"Authorization": f"Bearer {login(client, email)['access_token']}"}


@pytest.fixture()
def user_headers(client, regular_user):
    return bearer(client, regular_user.email)


@pytest.fixture()
def other_headers(client, other_user):
    return bearer(client, other_user.email)


@pytest.fixture()
def admin_headers(client, admin_user):
    return bearer(client, admin_user.email)


@pytest.fixture()
def super_headers(client, super_admin_user):
    return bearer(client, super_admin_user.email)


@pytest.fixture()
def sample_service(app):
    service = Services(
        style="Haircut & Styling",
        description="Wash, cut and style",
        cost=50.0,
        duration=60,
    )
    db.session.add(service)
    db.session.commit()
    return service
