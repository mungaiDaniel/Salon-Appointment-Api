from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import DevelopmentConfig
from flask_cors import CORS
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config.from_object(DevelopmentConfig)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
JWTManager(app)
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.app_context().push()


from app.auth import views, model
from app.service import views, model
from app.assistances import views, model
from app.bookings import views, model

if __name__ == '__main__':
    app.run(debug=True)