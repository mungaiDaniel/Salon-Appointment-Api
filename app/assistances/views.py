from app.auth.model import user_schema
from flask import request, make_response, jsonify
from app import app, db
from app.assistances.model import UserServices, employee_schema, employees_schemas
from app.assistances.controllers import UserServicesControll
import logging
from app.auth.model import User
import json
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity,decode_token

@app.route('/employee/<int:user_id>/<int:service_id>', methods=['POST'])
def add_employee(service_id,user_id):
    session = db.session
    
    return UserServicesControll.create_assistanceServices(service_id=service_id, user_id=user_id, session=session)
    
    

@app.route('/employee/<int:user_id>', methods=['GET'])
def employee_NY_ID(user_id):
    employee = UserServices.query.filter_by(user_id=user_id).all()
    session = db.session
    for c, i in  session.query(User, UserServices).filter(User.id == UserServices.user_id).all():
        print("result".format(c.id, c.firstName))
    return employees_schemas.jsonify(employee)

