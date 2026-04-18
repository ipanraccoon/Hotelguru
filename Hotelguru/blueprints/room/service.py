from Hotelguru.extensions import db
from Hotelguru.blueprints.room.schemas import RoomRequestSchema, RoomResponseSchema, RoomStatusSchema, RoomListSchema
from Hotelguru.models.RoomStatus import RoomStatus
from Hotelguru.models.Hotel import Hotel
from Hotelguru.models.Room import Room
from sqlalchemy import Select, select, and_

class RoomService:

    @staticmethod
    def room_add(request):
        try:
            room = Room(**request)
            db.session.add(room)
            db.session.commit()

        except Exception as ex:
            return False, "room_add() error"
        return True, RoomResponseSchema().dump(room)

    @staticmethod
    def room_list_all():
        rooms = db.session.execute(select(Room)).scalars()
        return True, RoomResponseSchema().dump(rooms, many=True)