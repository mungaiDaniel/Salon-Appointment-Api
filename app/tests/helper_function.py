import json

def register_user(self):
    return self.client.post(
        '/users',
        data=json.dumps(dict(
            firstName='fa-firstname', lastName='la-lastname', email='fa_example@gmail.com', password='123456', location='uthiru waiyakiway', user_role='super_admin', phoneNumber='0727980611'
        )),
        content_type='application/json'
    )
    
def login_user(self):
    return self.client.post(
        '/login',
        data = json.dumps(dict(
            email='fa_example@gmail.com', password='123456'
        )),
        content_type='application/json'
    )
    
def post_service(self):
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
    
    return response