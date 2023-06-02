from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import DevelopmentConfig
from flask_cors import CORS
from app.database.database import db
from app.auth.views import user_v1
from app.assistances.views import assisstance_v1
from app.service.views import service_v1
from app.bookings.views import booking_v1


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
    JWTManager(app)
    CORS(app)
    db.init_app(app)
    app.app_context().push()
    app.register_blueprint(user_v1)
    app.register_blueprint(assisstance_v1)
    app.register_blueprint(service_v1)
    app.register_blueprint(booking_v1)
    

    return app

app = create_app('config.DevelopmentConfig')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
