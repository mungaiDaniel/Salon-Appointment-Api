"""App-level behaviour: health, error format, config and CORS."""

import pytest
from flask import Flask

from config import Config, ProductionConfig
from main import create_app


def test_health_endpoints(client):
    for url in ("/health", "/api/v1/health"):
        response = client.get(url)
        assert response.status_code == 200
        assert response.get_json() == {
            "status": "ok",
            "db": "connected",
            "service": "salon-appointment-api",
        }


def test_health_reports_503_when_database_is_down(client, monkeypatch):
    from app.database.database import db

    def boom(*_a, **_k):
        raise RuntimeError("db down")

    monkeypatch.setattr(db.session, "execute", boom)
    response = client.get("/health")
    assert response.status_code == 503
    assert response.get_json()["db"] == "disconnected"


def test_unknown_route_returns_json_404(client):
    response = client.get("/api/v1/nope")
    assert response.status_code == 404
    assert response.get_json()["code"] == "not_found"


def test_wrong_method_returns_json_405(client):
    response = client.delete("/api/v1/login")
    assert response.status_code == 405
    assert response.get_json()["status"] == 405


def test_malformed_json_is_handled(client):
    response = client.post("/api/v1/login", data="{not json", content_type="application/json")
    assert response.status_code == 422


def test_unexpected_errors_are_500_without_leaking_details(app, client):
    @app.get("/boom")
    def boom():
        raise RuntimeError("secret internal detail")

    app.config["PROPAGATE_EXCEPTIONS"] = False
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.get_json()["code"] == "internal_error"
    assert "secret" not in response.get_data(as_text=True)


def test_swagger_spec_and_ui_are_served(client):
    spec = client.get("/static/swagger.json")
    assert spec.status_code == 200
    assert "/api/v1/login" in spec.get_json()["paths"]
    assert client.get("/swagger/").status_code == 200


def test_cors_only_allows_configured_origins(client):
    allowed = client.get("/health", headers={"Origin": "http://localhost:3000"})
    denied = client.get("/health", headers={"Origin": "https://evil.example"})
    assert allowed.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"
    assert "Access-Control-Allow-Origin" not in denied.headers


def test_secret_key_is_required_outside_tests(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        Config.init_app(Flask(__name__))


def test_short_secret_key_is_rejected(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "too-short")
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        Config.init_app(Flask(__name__))


def test_production_requires_database_uri(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "x" * 40)
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = None
    with pytest.raises(RuntimeError, match="DATABASE_URI"):
        ProductionConfig.init_app(app)


def test_factory_builds_app_from_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "k" * 40)
    monkeypatch.setenv("DATABASE_URI", f"sqlite:///{tmp_path / 'x.db'}")
    monkeypatch.setenv("FLASK_CONFIG", "config.DevelopmentConfig")
    built = create_app()
    assert built.config["JWT_SECRET_KEY"] == "k" * 40
