import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "test-secret-key-32-bytes-minimum-length-key!"
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or "sqlite:///:memory:"


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-32-bytes-minimum-length-key!"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///salon_dev.db"
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///salon_prod.db"

    @classmethod
    def init_app(cls, app):
        if not os.environ.get("SECRET_KEY"):
            raise ValueError(
                "SECRET_KEY environment variable is required in production environment."
            )
