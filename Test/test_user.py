from app import db
from app.auth.model import User
from Test.test_base import BaseTestCase
import json

class TestUser(BaseTestCase):

    def test_user_create(self):
        user = User(firstName='fa-firstname', lastName='la-lastname', email='fa_example@gmail.com', password='123456', location='uthiru waiyakiway', user_role='user', phoneNumber='0727980611')
        db.session.add(user)
        db.session.commit()
        assert user in db.session

    def test_md5_encrpt(self):
    
        password = User.generate_password_hash('123456')

        user = User(firstName='fa-firstname', lastName='la-lastname', email='fa_example@gmail.com', password=password, location='uthiru waiyakiway', user_role='user', phoneNumber='0727980611')

        self.assertTrue(user.verify_password_hash("123456"))


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
            response = self.client.post("/login",
                                    data=json.dumps(
                                        dict(email='mama_example@gmail.com',  password='123456')),
                                    content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200) 
            self.assertTrue('access_token' in data.get('value'))
            self.assertEqual('SUCCESS.', data.get('message'))