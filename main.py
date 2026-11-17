"""Flask application factory."""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import select, text

from app.assistances.views import assistance_v1
from app.auth.model import User
from app.auth.views import user_v1
from app.bookings.views import booking_v1
from app.cli import register_cli
from app.database.database import db
from app.errors import error_response, register_error_handlers
from app.extensions import cors, jwt, limiter, migrate
from app.logging_config import setup_logging
from app.service.views import service_v1

SWAGGER_URL = "/swagger"
SWAGGER_SPEC_URL = "/static/swagger.json"


def create_app(config_object=None) -> Flask:
    """Build and configure the app.

    ``config_object`` may be a dotted path or class; it defaults to ``$FLASK_CONFIG`` and then
    ``config.DevelopmentConfig``. A local ``.env`` file is loaded first (never committed).
    """
    load_dotenv()
    config_object = config_object or os.environ.get("FLASK_CONFIG", "config.DevelopmentConfig")

    app = Flask(__name__)
    app.config.from_object(config_object)
    _resolve(config_object).init_app(app)

    setup_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cors.init_app(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    _register_jwt_callbacks()
    register_error_handlers(app)
    register_cli(app)

    for blueprint in (user_v1, assistance_v1, service_v1, booking_v1):
        app.register_blueprint(blueprint)
    app.register_blueprint(
        get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_SPEC_URL, config={"app_name": "Salon API"}),
        url_prefix=SWAGGER_URL,
    )

    @app.get("/health")
    @app.get("/api/v1/health")
    @limiter.exempt
    def health_check():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            app.logger.exception("Database health check failed")
            return jsonify({"status": "error", "db": "disconnected"}), 503
        return jsonify({"status": "ok", "db": "connected", "service": "salon-appointment-api"})

    return app


def _resolve(config_object):
    if isinstance(config_object, str):
        from werkzeug.utils import import_string

        return import_string(config_object)
    return config_object


def _register_jwt_callbacks() -> None:
    """Load the User for each token and return JSON (not HTML) for every auth failure."""

    @jwt.user_lookup_loader
    def load_user(_header, payload):
        return db.session.execute(select(User).filter_by(email=payload["sub"])).scalar_one_or_none()

    @jwt.user_lookup_error_loader
    def user_gone(_header, _payload):
        return error_response(401, "user_not_found", "The account for this token no longer exists.")

    @jwt.unauthorized_loader
    def missing_token(reason):
        return error_response(401, "authorization_required", reason)

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error_response(401, "invalid_token", reason)

    @jwt.expired_token_loader
    def expired_token(_header, _payload):
        return error_response(401, "token_expired", "The token has expired.")
