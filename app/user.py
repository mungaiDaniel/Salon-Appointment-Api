from app import db, ma

class Users(db.Model):
    
    __tablename__ = 'users'
    
    Id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    PhoneNumber = db.Column(db.Integer)
    Location = db.Column(db.String(100))
    
    
    def __init__(self, FirstName, LastName, Email, Password, PhoneNumber, Location):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Password = Password
        self.PhoneNumber = PhoneNumber
        self.Location = Location
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('Id', 'FirstName', 'LastName', 'Email', 'Password', 'PhoneNumber', 'Location')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True) 