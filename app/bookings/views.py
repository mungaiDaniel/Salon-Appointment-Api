from flask import request, Blueprint
from app.assistances.model import UserServices
from app.service.model import Services
from app.database.database import db
from app.schemas.schemas import services_schemas
from app.schemas.schemas import booking_schema
from app.bookings.controllers import BookingController
from flask_jwt_extended import jwt_required


booking_v1 = Blueprint('booking_v1', __name__, url_prefix='/api/v1')

@booking_v1.route('/employee_service/<int:employee_id>', methods=['GET'])
def get_userservices(employee_id):

    employ_services = Services.query \
        .join(UserServices, Services.id
              == UserServices.service_id) \
        .filter(UserServices.user_id == employee_id) \
    
    
    result = db.session.execute(employ_services)
    names = [row[0] for row in result]
    
    res = services_schemas.dump(names)
    
    
    return res

@booking_v1.route('/booking', methods=['POST'])
@jwt_required()
def book():
    
    data = request.get_json()
    session = db.session
    
    return BookingController.book_appointment(data, session=session)

@booking_v1.route('/booking', methods=['GET'])
def get_all_bookings():
    session = db.session
    
    return BookingController.get_all_bookings(session=session)

@booking_v1.route('/booking/<int:id>', methods=['GET'])
def get_one_booking(id):
    session = db.session
    
    result = BookingController.get_booking_by_id(id, session=session)
    
    return booking_schema.dump(result)




    
    
    

    