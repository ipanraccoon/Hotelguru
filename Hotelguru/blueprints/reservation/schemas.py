from datetime import datetime
from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested, Boolean, Date, DateTime
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reception.schemas import ReservationServiceResponseSchema


class ReservationRequestSchema(Schema):
    user_id = Integer(required=True)

    reserved_start_date = Date(required=True)
    reserved_end_date = Date(required=True)

    room_ids = List(Integer(), required=True)

class ReservationResponseSchema(Schema):
    id = Integer()

    user_id = Integer()

    reserved_start_date = Date()
    reserved_end_date = Date()

    status = String()



#class RoomSchema(Schema):
    #number = Integer()
    #beds = Integer()
    #kitchen = Boolean()

#class ReservationSchema(Schema):
    #reserved_start_date = String()
    #reserved_end_date = String()
    #status = String()
    #rooms = Nested(RoomSchema, many=True)
    #services = Nested(ReservationServiceResponseSchema, many=True)
    

    
