import json
from app.database.model import Services
from app.tests.test_base import BaseTestCase
from app.tests.helper_function import post_service

class TestServces(BaseTestCase):
    
    def test_init(self):
        self.new_service = Services(style='blowdry', description='straigtening is the art of blow darying your hair with hot iron to starightening it', cost=34.50, duration=2, user_id=1)
        
        self.assertTrue(type(self.new_service.id), int)
        self.assertEqual(type(self.new_service), Services)
        
    def service_post(self):
        response = post_service(self)
        self.assertEqual(response.status_code, 201)
        
        
        