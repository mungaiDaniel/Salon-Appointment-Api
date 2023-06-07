from app.database.database import db
from app.auth.model import User
from Test.test_base import BaseTestCase
import json

class TestUser(BaseTestCase):

    def test_new_user(self):

        data = {'firstName':'fa-firstname', 'lastName':'la-lastname', 'email':'fa_example@gmail.com', 'password':'123456', 'location' :'uthiru waiyakiway', 'phoneNumber' :'0727980611'}
        resp = self.client.post( 'api/v1/users', data=json.dumps(data), content_type='application/json' )
        self.assertEqual(resp.status_code, 201)

    def test_register_username_twice(self):
        data = {'firstName':'fa-firstname', 'lastName':'la-lastname', 'email':'fa_example@gmail.com', 'password':'123456', 'location' :'uthiru waiyakiway', 'phoneNumber' :'0727980611'}
        response = self.client.post('api/v1/users',
                                    data=json.dumps(data), content_type='application/json')
        new_user = {'firstName':'fa-firstname', 'lastName':'la-lastname', 'email':'fa_example@gmail.com', 'password':'123456', 'location' :'uthiru waiyakiway', 'phoneNumber' :'0727980611'}
        response = self.client.post('api/v1/users',
                                    data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_get_all_user(self):
        response = self.client.get('api/v1/users', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_user(self):
        data = {'firstName':'fa-firstname', 'lastName':'la-lastname', 'email':'fa_example@gmail.com', 'password':'123456', 'location' :'uthiru waiyakiway', 'phoneNumber' :'0727980611'}
        self.client.post( 'api/v1/users', data=json.dumps(data), content_type='application/json' )
        response = self.client.get('api/v1/users/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_superadmin(self):
        data = {'firstName':'fa-firstname', 'lastName':'la-lastname', 'email':'fa_example@gmail.com', 'password':'123456', 'location' :'uthiru waiyakiway', 'phoneNumber' :'0727980611'}
        self.client.post( 'api/v1/users', data=json.dumps(data), content_type='application/json' )
        response = self.client.get('api/v1/users/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_not_found(self):
        # test cant login a non user
        response = self.client.post('api/v1/login',
                                    data=json.dumps(
                                        {'email': 'wanjiruamungi@gmail.com','password': 'password'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

class LoginTest(BaseTestCase):

    def setUp(self):
        super(LoginTest, self).setUp()
        password = User.generate_password_hash("123456")
        user = User(firstName='ma-firstname', 
                    lastName='ma-lastname',
                    email='mama_example@gmail.com', 
                    password=password, 
                    location='uthiru waiyakiway', 
                    user_role='super_admin', 
                    phoneNumber='0727980611')
        db.session.add(user)
        db.session.commit()

    def test_login(self):
        response = self.client.post("api/v1/login",
                                data=json.dumps(
                                    dict(email='mama_example@gmail.com',  password='123456')),
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200) 
        self.assertTrue('access_token' in data.get('value'))
        self.assertEqual('SUCCESS.', data.get('message'))