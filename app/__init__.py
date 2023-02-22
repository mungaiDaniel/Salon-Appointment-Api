from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:username@localhost:5432/Salon_Api"
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
app.app_context().push()

from app.auth import routes

if __name__ == '__main__':
    app.run(debug=True)