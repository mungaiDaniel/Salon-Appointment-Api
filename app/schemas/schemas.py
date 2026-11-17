"""Marshmallow schemas: strict input validation and explicit output shapes.

Output schemas never expose password hashes.
"""

from datetime import timezone

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load, validate

PHONE_REGEX = r"^\+?[0-9][0-9\s\-]{6,18}$"


class _Input(Schema):
    class Meta:
        unknown = EXCLUDE  # ignore extras such as a client-supplied "user_role"


# ---------- input ----------
class RegisterSchema(_Input):
    firstName = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    lastName = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=128))
    phoneNumber = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.Regexp(PHONE_REGEX, error="Invalid phone number."),
    )
    location = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=100))

    @post_load
    def normalise(self, data, **_):
        data["email"] = data["email"].strip().lower()
        return data


class LoginSchema(_Input):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def normalise(self, data, **_):
        data["email"] = data["email"].strip().lower()
        return data


class ServiceInputSchema(_Input):
    style = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=500))
    cost = fields.Float(required=True, validate=validate.Range(min=0))
    duration = fields.Int(required=True, validate=validate.Range(min=1, max=24 * 60))


class BookingInputSchema(_Input):
    date = fields.DateTime(required=True)
    service_id = fields.Int(required=True)
    employee_id = fields.Int(load_default=None, allow_none=True)

    @post_load
    def to_naive_utc(self, data, **_):
        value = data["date"]
        if value.tzinfo is not None:
            data["date"] = value.astimezone(timezone.utc).replace(tzinfo=None)
        return data


# ---------- output ----------
class UserSchema(Schema):
    id = fields.Int()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
    phoneNumber = fields.Str()
    location = fields.Str()
    user_role = fields.Str()
    created = fields.DateTime(attribute="date_created")


class PublicEmployeeSchema(Schema):
    """What anonymous visitors may see about staff (no contact details)."""

    id = fields.Int()
    firstName = fields.Str()
    lastName = fields.Str()
    location = fields.Str()
    user_role = fields.Str()


class ServiceSchema(Schema):
    id = fields.Int()
    style = fields.Str()
    description = fields.Str()
    cost = fields.Float()
    duration = fields.Int()
    user_id = fields.Int()


class EmployeeServiceSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    service_id = fields.Int()


class BookingSchema(Schema):
    id = fields.Int()
    date = fields.DateTime()
    employee_id = fields.Int()
    user_id = fields.Int()
    service_id = fields.Int()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
public_employees_schema = PublicEmployeeSchema(many=True)
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
employee_service_schema = EmployeeServiceSchema()
employee_services_schema = EmployeeServiceSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

register_schema = RegisterSchema()
login_schema = LoginSchema()
service_input_schema = ServiceInputSchema()
booking_input_schema = BookingInputSchema()


def load_json(schema: Schema, payload) -> dict:
    """Validate a request body; a missing/non-object body is a validation error."""
    if not isinstance(payload, dict):
        raise ValidationError({"_schema": ["A JSON object body is required."]})
    return schema.load(payload)
