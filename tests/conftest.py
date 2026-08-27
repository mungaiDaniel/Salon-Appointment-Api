import os

os.environ.setdefault("DATABASE_URI", "sqlite:///:memory:")

import pytest
import json
from main import create_app
from app.database.database import db
from config import TestingConfig
from app.auth.model import User
from app.service.model import Services


@pytest.fixture(scope="function")
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def super_admin_user(app):
    password_hash = User.generate_password_hash("Admin123!")
    user = User(
        firstName="Super",
        lastName="Admin",
        email="superadmin@salon.com",
        password=password_hash,
        location="Headquarters",
        user_role="super_admin",
        phoneNumber="0700000000",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def admin_user(app):
    password_hash = User.generate_password_hash("Admin123!")
    user = User(
        firstName="Admin",
        lastName="Manager",
        email="admin@salon.com",
        password=password_hash,
        location="Branch Office",
        user_role="admin",
        phoneNumber="0722222222",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def regular_user(app):
    password_hash = User.generate_password_hash("User123!")
    user = User(
        firstName="Jane",
        lastName="Doe",
        email="jane.doe@salon.com",
        password=password_hash,
        location="Downtown",
        user_role="user",
        phoneNumber="0711111111",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def super_admin_headers(client, super_admin_user):
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"email": "superadmin@salon.com", "password": "Admin123!"}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    token = data["value"]["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def admin_headers(client, admin_user):
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"email": "admin@salon.com", "password": "Admin123!"}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    token = data["value"]["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def regular_user_headers(client, regular_user):
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"email": "jane.doe@salon.com", "password": "User123!"}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    token = data["value"]["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def sample_service(app):
    service = Services(
        style="Haircut & Styling",
        description="Premium haircut with professional wash and styling",
        cost=50.00,
        duration=60,
    )
    db.session.add(service)
    db.session.commit()
    return service
