from app.database.model import Users, UserServices, Bookings, booking_schema, bookings_schemas ,user_schema, users_schema, service_schema,services_schemas, Services
from flask import request, make_response, jsonify
from app import app, db
import logging
import json
import datetime
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity,decode_token

@app.route('/employee_service/<int:employee_id>', methods=['GET'])
def get_userservices(employee_id):


    # email = get_jwt_identity()


    employ_services = Services.query \
        .join(UserServices, Services.id
              == UserServices.service_id) \
        .filter(UserServices.user_id == employee_id) \
    
    
    result = db.session.execute(employ_services)
    names = [row[0] for row in result]
    print(":::::::::::::::::::::::>>>",names)
    
    res = services_schemas.jsonify(names)
    
    print('<><><><><><><><.', res)
    
    return res

@app.route('/booking', methods=['POST'])
@jwt_required()
def book():
    
    email = get_jwt_identity()
    user = Users.query.filter_by(email=email).first()
    
    
    data = request.get_json()
    employee = data['employee_id']
    employee_id = Users.query.filter_by(id = employee).first()
    
    
    
    
    service = data['service_id']
    service_id = Services.query.filter_by(id= service).first()
    
    
    bookings = Bookings(employee_id=employee_id.id, service_id=service_id.id, user_id=user.id, time=datetime.datetime.now())
    
    db.session.add(bookings)
    db.session.commit()
    
    return booking_schema.jsonify(bookings)
    
    
    
    

    