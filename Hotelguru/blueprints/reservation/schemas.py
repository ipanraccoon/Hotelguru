from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested, Boolean
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema

class RoomSchema(Schema):
    number = Integer()
    beds = Integer()
    kitchen = Boolean()

class ReservationSchema(Schema):
    reserved_start_date = String()
    reserved_end_date = String()
    status = String()
    rooms = Nested(RoomSchema, many=True)
    invoice = fields.Nested(InvoiceSchema)
    

    
