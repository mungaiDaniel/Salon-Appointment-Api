import os

postgre_local_base = "postgresql://postgres:username@localhost/gerente"

class Config(object):
        DEBUG = True
        TESTING = False
        CSRF_ENABLED = True
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess'
    
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    
class TestingConfig(Config):
        TESTING = False
        DEBUG = True
        DEVELOPMENT = False
        TESTING = True
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:username@localhost/test-salon-api"

        
class DevelopmentConfig(Config):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = postgre_local_base
        DEBUG = True
        DEVELOPMENT = True
        
class ProductionConfig(Config):
        
        SECRET_KEY = 'my_precious'
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
        
        
        
