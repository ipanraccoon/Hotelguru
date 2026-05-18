from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested, Boolean
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reception.schemas import ReservationServiceResponseSchema

class RoomSchema(Schema):
    number = Integer()
    beds = Integer()
    kitchen = Boolean()

class ReservationSchema(Schema):
    reserved_start_date = String()
    reserved_end_date = String()
    status = String()
    rooms = Nested(RoomSchema, many=True)
    services = Nested(ReservationServiceResponseSchema, many=True)
    

    
