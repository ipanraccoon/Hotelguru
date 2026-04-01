from marshmallow import Schema
from apiflask.fields import Integer, String, Email
from apiflask.validators import Length, Email, OneOf



class LoginSchema(Schema):
    email = String(required=True,validate=Email())
    password = String(required=True)

class UserSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    phone = String()
