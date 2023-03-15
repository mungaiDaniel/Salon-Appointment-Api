
import unittest
from app import app, db
from config import TestingConfig



class BaseTestCase (unittest.TestCase):
    
    def setUp(self):
        with app.app_context():
            app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:username@localhost:5432/test-api"
            db.drop_all()
            db.create_all()
            self.app = app.test_client()
            
    # def tearDown(self):
    #     with app.app_context():
    #         db.session.remove()
    #         db.drop_all()
   