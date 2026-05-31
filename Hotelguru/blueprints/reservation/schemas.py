from datetime import datetime, date
from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested, Boolean, Date, DateTime
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reception.schemas import ReservationServiceResponseSchema


def _format_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value[:10]
    return str(value)


def _reservation_to_dict(reservation):
    return {
        "id": reservation.id,
        "user_id": reservation.user_id,
        "reserved_start_date": _format_date(reservation.reserved_start_date),
        "reserved_end_date": _format_date(reservation.reserved_end_date),
        "status": reservation.status,
    }


class ReservationRequestSchema(Schema):
    user_id = Integer(required=True)

    reserved_start_date = Date(required=True)
    reserved_end_date = Date(required=True)

    room_ids = List(Integer(), required=True)

class ReservationResponseSchema(Schema):
    id = Integer()
    user_id = Integer()
    reserved_start_date = String()
    reserved_end_date = String()
    status = String()


def dump_reservation(obj, many=False):
    if many:
        return [_reservation_to_dict(item) for item in obj]
    return _reservation_to_dict(obj)



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
    

    
