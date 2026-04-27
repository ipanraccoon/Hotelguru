from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested
from Hotelguru.blueprints.service.schemas import ServiceResponseSchema

class AddServiceSchema(Schema):
    service_id = Integer(required=True)
    quantity = Integer()

class ReservationServiceResponseSchema(Schema):
    service = Nested(ServiceResponseSchema)
    quantity = Integer()
