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