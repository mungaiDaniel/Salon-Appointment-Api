from flask import request, make_response, jsonify
from app.assistances.model import UserServices
from app.service.model import Services, service_schema, services_schemas
from app import app, db
from app.bookings.model import booking_schema, bookings_schemas
from app.auth.model import User
from app.bookings.controllers import BookingController
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity,decode_token

@app.route('/employee_service/<int:employee_id>', methods=['GET'])
def get_userservices(employee_id):

    employ_services = Services.query \
        .join(UserServices, Services.id
              == UserServices.service_id) \
        .filter(UserServices.user_id == employee_id) \
    
    
    result = db.session.execute(employ_services)
    names = [row[0] for row in result]
    
    res = services_schemas.jsonify(names)
    
    
    return res

@app.route('/booking', methods=['POST'])
@jwt_required()
def book():
    
    data = request.get_json()
    session = db.session
    
    return BookingController.book_appointment(data, session=session)

@app.route('/booking', methods=['GET'])
def get_all_bookings():
    session = db.session
    
    return BookingController.get_all_bookings(session=session)

@app.route('/booking/<int:id>', methods=['GET'])
def get_one_booking(id):
    session = db.session
    
    result = BookingController.get_booking_by_id(id, session=session)
    
    return booking_schema.jsonify(result)


    
    
    

    