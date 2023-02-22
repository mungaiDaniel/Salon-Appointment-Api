from flask_httpauth import HTTPTokenAuth
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

jwt = Serializer('top secret')

refresh_jwt = Serializer('telelelele')

auth = HTTPTokenAuth('Bearer')