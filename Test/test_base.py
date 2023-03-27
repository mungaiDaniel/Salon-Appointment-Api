
from unittest import TestCase
from config import TestingConfig
from app import  db, app

class BaseTestCase(TestCase):
    
   def setUp(self):
        self.app = app
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app.testing = True
        db.drop_all()
        db.create_all()
            
