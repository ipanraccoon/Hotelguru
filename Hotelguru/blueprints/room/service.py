from datetime import date
from Hotelguru.extensions import db
from Hotelguru.blueprints.room.schemas import RoomRequestSchema, RoomResponseSchema, RoomStatusSchema, RoomListSchema
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.ReservationRoom import ReservationRoom
from Hotelguru.models.RoomStatus import RoomStatus
from Hotelguru.models.Hotel import Hotel
from Hotelguru.models.Room import Room
from sqlalchemy import Select, select, and_

class RoomService:

    @staticmethod
    def room_add(request):
        try:
           hotel = db.session.get(Hotel, request["hotel_id"])
           status = db.session.get(RoomStatus, request["status_id"])

           if not hotel:
               return False, "Invalid hotelID"
           if not status:
               return False, "Invalid statusID"

           room = Room()
           room.number = request["number"]
           room.beds=int(request["beds"])
           room.kitchen=request["kitchen"]
           room.price=int(request["price"])
           room.hotel_id=request["hotel_id"]
           room.status_id=request["status_id"]
            
                
           db.session.add(room)
           db.session.commit()

           return True, RoomResponseSchema().dump(room)

        except Exception as ex:
            db.session.rollback()
            return False, "room_add() error"

    @staticmethod
    def room_list_all():
        rooms = db.session.execute(select(Room)).scalars().all()
        return True, RoomResponseSchema().dump(rooms, many=True)

    @staticmethod
    def room_list_hotel(hid):
       if hid is None:
           rooms = db.session.execute(select(Room)).scalars().all()
       else:
           rooms = db.session.execute(select(Room).filter(Room.hotel_id == hid)).scalars().all()
       return True, RoomListSchema().dump(rooms, many = True)


    @staticmethod
    def room_update(rid, request):
        try:
            room = db.session.get(Room, rid)

            if room:
                room.number = request["number"]
                room.beds = int(request["beds"])
                room.kitchen = request["kitchen"]
                room.price = int(request["price"])

                db.session.commit()
                return True, RoomResponseSchema().dump(room)
        except Exception as ex:
            db.session.rollback()
            return False, "room_update() error!"


    @staticmethod
    def room_delete(rid):
        try:
            room = db.session.get(Room, rid)
            if room:
                db.session.delete(room)
                db.session.commit()
        except Exception as ex:
            db.session.rollback()
            return False, "room_delete() error!"
        return True, "OK!"

    @staticmethod
    def room_list_date(start_date, end_date):
        reserved_rooms = (select(ReservationRoom.room_id)
                          .join(Reservation)
                          .where(and_
                                 (
                                     Reservation.status != "Cancelled",
                                     Reservation.reserved_start_date <= end_date,
                                     Reservation.reserved_end_date >= start_date
                                 )))
        rooms = db.session.execute(
            select(Room).where(~Room.id.in_(reserved_rooms))
            ).scalars().all()

        return True, RoomListSchema().dump(rooms, many=True)

    @staticmethod
    def room_list_available(city, start_date, end_date):
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        reserved_rooms = (
            select(ReservationRoom.room_id)
            .join(Reservation)
            .join(Room, ReservationRoom.room_id == Room.id)
            .join(Hotel, Room.hotel_id == Hotel.id)
            .where(and_(
                Hotel.city == city,
                Reservation.status != "Cancelled",
                Reservation.reserved_start_date <= end_date,
                Reservation.reserved_end_date >= start_date,
            ))
        )
        rooms = db.session.execute(
            select(Room)
            .join(Hotel, Room.hotel_id == Hotel.id)
            .where(Hotel.city == city)
            .where(~Room.id.in_(reserved_rooms))
        ).scalars().all()

        return True, RoomListSchema().dump(rooms, many=True)

    @staticmethod
    def room_list_avalible(city, start_date, end_date):
        return RoomService.room_list_available(city, start_date, end_date)
