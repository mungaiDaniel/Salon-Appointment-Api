"""Application configuration, driven entirely by environment variables.

Select a config with ``FLASK_CONFIG`` (default ``config.DevelopmentConfig``).
``SECRET_KEY`` is mandatory for every config except ``TestingConfig``.
"""

import os
from datetime import timedelta


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "60")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_DAYS", "7")))
    CORS_ORIGINS = _csv(os.environ.get("CORS_ORIGINS", "http://localhost:3000"))
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_ENABLED = True
    RATELIMIT_LOGIN = os.environ.get("RATELIMIT_LOGIN", "10 per minute")
    RATELIMIT_REGISTER = os.environ.get("RATELIMIT_REGISTER", "20 per hour")

    @classmethod
    def init_app(cls, app):
        secret = os.environ.get("SECRET_KEY")
        if not secret or len(secret) < 32:
            raise RuntimeError(
                "SECRET_KEY must be set (at least 32 characters). Generate one with: "
                'python -c "import secrets; print(secrets.token_hex(32))"'
            )
        app.config["SECRET_KEY"] = secret
        app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY") or secret


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///salon_dev.db"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        if not app.config["SQLALCHEMY_DATABASE_URI"]:
            raise RuntimeError("DATABASE_URI must be set in production.")


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test-only-secret-key-not-for-real-use-0123456789"
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or "sqlite:///:memory:"
    RATELIMIT_ENABLED = False

    @classmethod
    def init_app(cls, app):
        pass
