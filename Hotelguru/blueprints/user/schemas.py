from marshmallow import Schema, fields
from apiflask import Schema
from apiflask.fields import Integer, String, Email
from apiflask.validators import Length, Email



class LoginSchema(Schema):
    email = String(required=True,validate=Email())
    password = String(required=True)

class UserSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    phone = String()

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
