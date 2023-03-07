import os

basedir = os.path.abspath(os.path.dirname(__file__))
postgre_local_base = "postgresql://postgres:username@localhost:5432/Salon_api"

class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        DEBUG = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
class DevelopmentConfig(Config):
        
        SQLALCHEMY_DATABASE_URI = postgre_local_base
        DEBUG = True
        
class TestingConfig(Config):
        
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:username@localhost:5432/salon_test"
        
class ProductionConfig(Config):
        
        SECRET_KEY = 'my_precious'
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
        
app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
        
        
