from app import db
from app.service.model import Services
from Test.test_base import BaseTestCase
import json
from Test.helper_function import login_user

class TestService(BaseTestCase):

    def create_service(self):

        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("access_token", result)
        new_servces = {
        'style': 'blowdry',
        'description': 'straigtening is the art of blow darying your hair with hot iron to starightening it',
        'cost': 34.50,
        'duration': 2,
        'user_id': 1
    
        }
        response = self.client.post('/stylings', data=json.dumps(new_servces),
                                headers={'Authorization': f'Bearer{result["access_token"]}',
                                         'Content-Type': 'application' '/json'})
        self.assertEqual(response.status_code, 201)