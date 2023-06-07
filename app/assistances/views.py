from app.schemas.schemas import user_schema
from flask import Blueprint
from app.schemas.schemas import  employees_schemas
from app.database.database import db
from app.assistances.model import UserServices
from app.assistances.controllers import UserServicesControll
from app.auth.model import User

assisstance_v1 = Blueprint('assisstance_v1', __name__, url_prefix='/api/v1')

@assisstance_v1.route('/employee/<int:user_id>/<int:service_id>', methods=['POST'])
def add_employee(service_id,user_id):
    session = db.session
    new_employee = UserServicesControll.create_assistanceServices(service_id=service_id, user_id=user_id, session=session)
    return new_employee
    
@assisstance_v1.route('/employee/<int:user_id>', methods=['GET'])
def employee_NY_ID(user_id):
    employee = UserServices.query.filter_by(user_id=user_id).all()
    session = db.session
    for c, i in  session.query(User, UserServices).filter(User.id == UserServices.user_id).all():
        print("result".format(c.id, c.firstName))
    return employees_schemas.dump(employee)

