import os

postgre_local_base = "postgresql://postgres:username@localhost/gerente"
    
class TestingConfig():
        
        TESTING = True
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:username@localhost/testsalon"

        
class DevelopmentConfig():
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
        DEBUG = True
        DEVELOPMENT = True
        
class ProductionConfig():
        
        SECRET_KEY = 'my_precious'
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
        PRODUCTION = True
        
# postgres://username:7g9dB25gyhqv09nvOisRgIjg6Qa8tC1o@dpg-chvfe51mbg5b5peu6vcg-a.oregon-postgres.render.com/salon_online