from app.bookings.model import Bookings
from app.database.database import db
from app.schemas.schemas import booking_schema, bookings_schemas
from flask_jwt_extended import  get_jwt_identity
from app.auth.model import User
from app.service.model import Services

class BookingController:
    
    model = Bookings
    
    @classmethod
    def book_appointment(cls, data, session):
        
        email = get_jwt_identity()
        user_id = User.query.filter_by(email=email).first()
        
        employee = data.get('employee_id')
        employee_id = User.query.filter_by(id = employee).first()
        
        service = data.get('service_id')
        service_id = Services.query.filter_by(id= service).first()
        
        bookings = cls.model(
            date = data.get('date'),
            employee_id = employee_id.id,
            service_id = service_id.id,
            user_id = user_id.id
        )
        cls.model.save(bookings, session=session)
        
        return booking_schema.dump(bookings)
        
    @classmethod
    def get_all_bookings(cls, session):
        book = Bookings.get_all(cls.model, session)
        
        return bookings_schemas.dump(book)
    
    @classmethod
    def get_booking_by_id(cls, id, session):
        
        book = Bookings.get_one(cls.model, id, session)
        
        return book
        
        
        