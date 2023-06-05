from main import db
from app.service.model import Services
from Test.test_base import BaseTestCase
import json
from Test.helper_function import login_user, register_user

class TestService(BaseTestCase):

    def test_create_service(self):
        register_user(self)
        response = login_user(self)
        result = json.loads(response.data)
        print('<><><><>', result['value']['access_token'])
        self.assertIn("access_token", result['value'])
        new_servces = {
        'style': 'blowdry',
        'description': 'straigtening is the art of blow darying your hair with hot iron to starightening it',
        'cost': 34.50,
        'duration': 2
        }
        token = result["value"]["access_token"]
     
        response = self.client.post('api/v1/stylings', data=json.dumps(new_servces),
                                headers={'Authorization': f"Bearer {token}",
                                         'Content-Type': 'application' '/json'})
        self.assertEqual(response.status_code, 200)