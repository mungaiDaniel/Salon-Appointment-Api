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

    def test_get_all_services(self):
        response = self.client.get('api/v1/stylings', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_service(self):
        register_user(self)
        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("access_token", result['value'])
        new_servces = {
        'style': 'blowdry',
        'description': 'straigtening is the art of blow darying your hair with hot iron to starightening it',
        'cost': 34.50,
        'duration': 2
        }
        token = result["value"]["access_token"]
     
        self.client.post('api/v1/stylings', data=json.dumps(new_servces),
                                headers={'Authorization': f"Bearer {token}",
                                         'Content-Type': 'application' '/json'})
        
        response2 = self.client.get('api/v1/stylings', content_type='application/json')
        self.assertEqual(response2.status_code, 200)

    def test_update_service(self):
        register_user(self)
        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("access_token", result['value'])
        new_servces = {
        'style': 'blowdry',
        'description': 'straigtening is the art of blow darying your hair with hot iron to starightening it',
        'cost': 34.50,
        'duration': 2
        }
        token = result["value"]["access_token"]
     
        self.client.post('api/v1/stylings', data=json.dumps(new_servces),
                                headers={'Authorization': f"Bearer {token}",
                                         'Content-Type': 'application' '/json'})
        update_service ={
            'style': 'treatment',
        'description': 'straigtening is the art of blow darying your hair with hot iron to starightening it',
        'cost': 1000.50,
        'duration': 3

        }
        
        response2 = self.client.put('api/v1/stylings/1', data=json.dumps(update_service) , headers={'Authorization': f"Bearer {token}",
                                         'Content-Type': 'application' '/json'})
        self.assertEqual(response2.status_code, 200)
    