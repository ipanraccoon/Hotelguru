from datetime import datetime

from sqlalchemy import select

from Hotelguru.extensions import db

from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.ReservationRoom import ReservationRoom
from Hotelguru.models.Room import Room

from .schemas import ReservationResponseSchema


class ReservationService:


    @staticmethod
    def create_reservation(request):

        try:

            room_ids=request["room_ids"]


            rooms=(
                db.session.execute(
                    select(Room).where(
                        Room.id.in_(room_ids)
                    )
                ).scalars().all()
            )


            if not rooms:
                return False,"Rooms not found"


            for room in rooms:

                if not ReservationService.room_available(
                    room.id,
                    request["reserved_start_date"],
                    request["reserved_end_date"]
                ):
                    return (
                       False,
                       f"Room {room.id} unavailable"
                    )


            reservation=Reservation(
                user_id=request["user_id"],
                reserved_start_date=request[
                   "reserved_start_date"
                ],
                reserved_end_date=request[
                   "reserved_end_date"
                ],
                status="pending",
                created_at=datetime.utcnow()
            )

            db.session.add(
                reservation
            )

            db.session.flush()


            for room in rooms:

                reserved_room=ReservationRoom(
                    reservation_id=reservation.id,
                    room_id=room.id,
                    price_per_night=room.price
                )

                db.session.add(
                    reserved_room
                )


            db.session.commit()

        except Exception:
            db.session.rollback()
            return False,"Reservation failed"


        return (
            True,
            ReservationResponseSchema().dump(
                reservation
            )
        )


    @staticmethod
    def room_available(
        room_id,
        start_date,
        end_date
    ):

        conflicts=(
            db.session.execute(
                select(Reservation)
                .join(ReservationRoom)
                .where(
                    ReservationRoom.room_id==room_id,
                    Reservation.reserved_start_date
                        < end_date,
                    Reservation.reserved_end_date
                        > start_date
                )
            ).scalar_one_or_none()
        )


        return conflicts is None


    @staticmethod
    def approve_reservation(id):

        try:

            reservation=(
                db.session.execute(
                    select(Reservation)
                    .filter_by(id=id)
                ).scalar_one()
            )

            reservation.status="approved"

            db.session.commit()

        except Exception:
            return False,"Approval failed"


        return (
            True,
            ReservationResponseSchema().dump(
                reservation
            )
        )
