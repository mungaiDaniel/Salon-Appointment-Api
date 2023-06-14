from flask import Flask
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from app.database.database import db
from app.auth.views import user_v1
from app.assistances.views import assisstance_v1
from app.service.views import service_v1
from app.bookings.views import booking_v1
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT =get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name':'Salon Gerente'
        }
    )
    JWTManager(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    app.app_context().push()
    app.register_blueprint(user_v1)
    app.register_blueprint(assisstance_v1)
    app.register_blueprint(service_v1)
    app.register_blueprint(booking_v1)
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)
    

    return app

app = create_app('config.DevelopmentConfig')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
