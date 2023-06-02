from marshmallow import Schema

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password', 'phoneNumber', 'location', 'user_role', 'created')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Employeeschema(Schema):
    class Meta:
        fields = ('id', 'user_id', 'service_id')
        
employee_schema = Employeeschema()
employees_schemas = Employeeschema(many=True)

class Serviceschema(Schema):
    class Meta:
        fields = ('id', 'style', 'description', 'cost', 'duration', 'user_id')
        
service_schema = Serviceschema()
services_schemas = Serviceschema(many=True)

class Bookingschema(Schema):
    class Meta:
        fields = ('id', 'date', 'time' ,'employee_id' ,'user_id', 'service_id')
        
booking_schema = Bookingschema()
bookings_schemas = Bookingschema(many=True)