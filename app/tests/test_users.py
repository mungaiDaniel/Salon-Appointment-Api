from app import db
from app.database.model import Users
import json
from app.tests.test_base import BaseTestCase
import datetime
from app.tests.helper_function import register_user, login_user

class TestUsers(BaseTestCase):
    
    def test_user_created(self):
        
        user = Users(firstName='fa-firstname', lastName='la-lastname', email='fa_example@gmail.com', password='123456', location='uthiru waiyakiway', user_role='user', phoneNumber='0727980611')
        
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        
    def test_md5_encrpt(self):
        
        password = Users.generate_password_hash('123456')
        
        user = Users(firstName='fa-firstname', lastName='la-lastname', email='fa_example@gmail.com', password=password, location='uthiru waiyakiway', user_role='user', phoneNumber='0727980611')
        
        self.assertTrue(user.verify_password_hash("123456"))
        
    # def test_login(self):
    #     response = self.app.post("/login",
    #                              data=json.dumps(
    #                                  dict(email='fa_example@gmail.com', password='123456')),
    #                              content_type='application/json')
    #     data = json.loads(response.data)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('access_token' in data.get('message'))
        
