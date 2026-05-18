from apiflask import Schema
from apiflask.fields import Integer, String

class ServiceResponseSchema(Schema):
    id = Integer()
    name = String()
    price = Integer()

