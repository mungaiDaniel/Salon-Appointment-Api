# Salon-Appointment-Api
This is a salon application project whereby users can book for appointments , register and login to an account , admin can apgrade a user to an employee and admin can post new hair salon styles.

Using Flask to build a rest API server with swagger documentation

Intergration with flask_sqlalchemy, Flask, flask_marshmallow, flask_jwt_extended, pytest and flask_cors

### Extension:
- Flask:  [Flask](https://flask.palletsprojects.com/en/2.3.x/)

- SQL ORM: [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

- Testing: [Pytest](https://docs.pytest.org/en/7.3.x/)

- Oauth: [flask_jwt_extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

## Installation

install with pip:

```
$ pip install -r requirements.txt

```

## Flask Application Structure

```
|──────app/
| |────__init__.py
| |────assisstances/
| | |────controllers.py
| | |────model.py
| | |────views.py
| |────auth/
| | |────controllers.py
| | |────model.py
| | |────views.py
| |────booking/
| | |────controllers.py
| | |────model.py
| | |────views.py
| |────service/
| | |────controllers.py
| | |────model.py
| | |────views.py
|──────manage.py
|──────Tests/
| | |────helper_function.py
| | |────test_base.py
| | |────test_service.py
| | |────test_user.py
```
## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
## Run Flask
### Run flask for develop
```
$ FLASK_APP=manage.py python -m flask run
```

## Unittest
```
$ coverage run -m pytest 
```
## Endpoints