from flask import Flask
from config import Config , app_config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
app.app_context().push()






from app.api.auth import views 
from app.api.service import views
from app.api.assistances import views
from app.api.bookings import views

if __name__ == '__main__':
    app.run(debug=True)