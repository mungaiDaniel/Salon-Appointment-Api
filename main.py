import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from sqlalchemy import text
from app.logging_config import setup_logging
from app.database.database import db
from app.auth.views import user_v1
from app.assistances.views import assisstance_v1
from app.service.views import service_v1
from app.bookings.views import booking_v1


def create_app(config_filename=None):
    app = Flask(__name__)

    if config_filename is None:
        config_filename = os.environ.get("FLASK_CONFIG", "config.DevelopmentConfig")

    if isinstance(config_filename, str):
        app.config.from_object(config_filename)
    else:
        app.config.from_object(config_filename)

    setup_logging(app)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Salon Gerente"}
    )

    JWTManager(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    @app.route("/health", methods=["GET"])
    @app.route("/api/v1/health", methods=["GET"])
    def health_check():
        try:
            db.session.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            app.logger.error(f"Database health check failed: {e}")
            db_status = "disconnected"
            return jsonify({"status": "error", "db": db_status, "message": str(e)}), 500

        return jsonify({"status": "ok", "db": db_status, "service": "salon-appointment-api"}), 200

    app.register_blueprint(user_v1)
    app.register_blueprint(assisstance_v1)
    app.register_blueprint(service_v1)
    app.register_blueprint(booking_v1)
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


app = create_app(os.environ.get("FLASK_CONFIG", "config.DevelopmentConfig"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
