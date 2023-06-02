import os

postgre_local_base = "postgresql://postgres:username@localhost/gerente"
    
class TestingConfig():
        
        TESTING = True
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:username@localhost/testsalon"

        
class DevelopmentConfig():
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = postgre_local_base
        DEBUG = True
        DEVELOPMENT = True
        
class ProductionConfig():
        
        SECRET_KEY = 'my_precious'
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
        
        
        
