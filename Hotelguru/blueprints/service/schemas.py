from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length


class ServiceResponseSchema(Schema):
    id = Integer()
    name = String()
    price = Integer()
    hotel_id = Integer()


class ServiceRequestSchema(Schema):
    hotel_id = Integer(required=True)
    name = String(required=True, validate=Length(max=30))
    price = Integer(required=True)


class ServiceUpdateSchema(Schema):
    name = String(validate=Length(max=30))
    price = Integer()
