import json
from app.auth.model import User
from main import db
def register_user(self):
    return self.client.post(
        'api/v1/users',
        data=json.dumps(dict(
            firstName='ma-firstname', 
                        lastName='ma-lastname',
                        email='mama_example@gmail.com', 
                        password='123456', 
                        location='uthiru waiyakiway', 
                        user_role='super_admin', 
                        phoneNumber='0727980611'
        )),
        content_type='application/json'
    )
    
def login_user(self):
    return self.client.post(
        "api/v1/login",
        data = json.dumps(dict(
           email='mama_example@gmail.com',  password='123456'
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

def create_test_user(
        firstName='ma-firstname', 
        lastName='ma-lastname',
        email='mama_example@gmail.com', 
        password='123456', 
        location='uthiru waiyakiway', 
        user_role='super_aadmin', 
        phoneNumber='0727980611',
):
    user = User.query.filter_by(email='mama_example@gmail.com').first()

    if user is None:

        user = User(
        firstName = firstName,
        lastName = lastName,
        email=email,
        password= password,
        location= location,
        user_role = user_role,
        phoneNumber = phoneNumber,
        )
        db.session.add(user)
        db.session.commit()

        return user
    else:
        return {
            "messge": "No user found"
        }