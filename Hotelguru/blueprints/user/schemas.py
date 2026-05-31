from apiflask import Schema
from apiflask.fields import Integer, String, Email, List, Nested
from apiflask.validators import Length, Email



class LoginSchema(Schema):
    email = String(required=True,validate=Email())
    password = String(required=True)

class UserSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    phone = String()
    address = String()
    token = String()

class RoleSchema(Schema):
    id = Integer()
    name = String()

class RegisterSchema(Schema):
    name = String(required=True, validate=Length(max=30))
    email = String(required=True, validate=Email())
    password = String(required=True, validate=Length(min=6))
    phone = String(required=True, validate=Length(max=30))

class UserUpdateSchema(Schema):
    name = String(validate=Length(max=30))
    email = String(validate=Email())
    phone = String(validate=Length(max=30))
    address = String(validate=Length(max=100))

class AssignRoleSchema(Schema):
    role_id = Integer(required=True)

class PayloadSchema(Schema):
    user_id = Integer()
    roles  = List(Nested(RoleSchema))
    exp = Integer()