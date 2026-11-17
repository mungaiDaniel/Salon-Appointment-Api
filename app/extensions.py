"""Flask extension instances, created unbound and initialised in the app factory."""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

from app.database.database import db

jwt = JWTManager()
migrate = Migrate()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)

__all__ = ["db", "jwt", "migrate", "cors", "limiter"]
