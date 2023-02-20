from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:username@localhost:5432/salon_api"
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import routes, user

if __name__ == '__main__':
    app.run(debug=True)