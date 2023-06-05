import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from main import create_app
from base_model import Base
from app.database.database import db
from app.auth.model import User
from main import create_app
from config import TestingConfig

app = create_app('config.TestingConfig')


class BaseTestCase(unittest.TestCase):
   
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.app = app
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app.testing = True
        db.create_all()

    
       

if __name__ == '__main__':
    unittest.main()