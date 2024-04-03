import os

postgre_local_base = "postgresql://postgres:username@localhost/salons"
    
class TestingConfig():
        
        TESTING = True
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = "postgres://salongerentedatabase_user:k5GfZTZVNBArKrjNToOoKU14On9jKY58@dpg-co6j8ua0si5c73cglg60-a.oregon-postgres.render.com/salongerentedatabase"

        
class DevelopmentConfig():
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = postgre_local_base
        DEBUG = True
        DEVELOPMENT = True
        
class ProductionConfig():
        
        SECRET_KEY = 'my_precious'
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

        # postgres://salongerentedatabase_user:k5GfZTZVNBArKrjNToOoKU14On9jKY58@dpg-co6j8ua0si5c73cglg60-a.oregon-postgres.render.com/salongerentedatabase