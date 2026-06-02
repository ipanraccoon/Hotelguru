from datetime import datetime, date
from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested, Boolean, Date, DateTime


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


def _reservation_nights(reservation):
    start = reservation.reserved_start_date
    end = reservation.reserved_end_date
    if isinstance(start, str):
        start = date.fromisoformat(start[:10])
    if isinstance(end, str):
        end = date.fromisoformat(end[:10])
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()
    diff = end - start
    return diff.days if diff.days > 0 else 1


def _reservation_to_dict(reservation, detailed=False):
    result = {
        "id": reservation.id,
        "user_id": reservation.user_id,
        "reserved_start_date": _format_date(reservation.reserved_start_date),
        "reserved_end_date": _format_date(reservation.reserved_end_date),
        "status": reservation.status,
    }
    if not detailed:
        return result

    nights = _reservation_nights(reservation)
    rooms = []
    for reservation_room in reservation.rooms:
        room = reservation_room.rooms
        rooms.append({
            "id": room.id,
            "number": room.number,
            "beds": room.beds,
            "kitchen": room.kitchen,
            "price_per_night": reservation_room.price_per_night,
            "total_price": reservation_room.price_per_night * nights,
            "status": room.status.name if room.status else None,
        })

    services = []
    for reservation_service in reservation.services:
        services.append({
            "service_id": reservation_service.service_id,
            "name": reservation_service.service.name,
            "price": reservation_service.service.price,
            "quantity": reservation_service.quantity,
            "total_price": reservation_service.service.price * reservation_service.quantity,
        })

    result["nights"] = nights
    result["rooms"] = rooms
    result["services"] = services
    return result


class ReservationRequestSchema(Schema):
    reserved_start_date = Date(required=True)
    reserved_end_date = Date(required=True)

    room_ids = List(Integer(), required=True)

class ReservationRoomDetailSchema(Schema):
    id = Integer()
    number = Integer()
    beds = Integer()
    kitchen = Boolean()
    price_per_night = Integer()
    total_price = Integer()
    status = String()


class ReservationServiceDetailSchema(Schema):
    service_id = Integer()
    name = String()
    price = Integer()
    quantity = Integer()
    total_price = Integer()


class ReservationResponseSchema(Schema):
    id = Integer()
    user_id = Integer()
    reserved_start_date = String()
    reserved_end_date = String()
    status = String()
    nights = Integer()
    rooms = List(Nested(ReservationRoomDetailSchema))
    services = List(Nested(ReservationServiceDetailSchema))


def dump_reservation(obj, many=False, detailed=False):
    if many:
        return [_reservation_to_dict(item, detailed=detailed) for item in obj]
    return _reservation_to_dict(obj, detailed=detailed)
