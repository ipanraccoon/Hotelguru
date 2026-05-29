from datetime import datetime, date
from Hotelguru.extensions import db
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.ReservationRoom import ReservationRoom
from Hotelguru.models.Room import Room
from Hotelguru.blueprints.reservation.schemas import ReservationResponseSchema


class ReservationService:

    @staticmethod
    def reservation_add(data):
        try:
            resevation = Reservation()

            resevation.user_id = data["user_id"]

            resevation.reserved_start_date = data["reserved_start_date"]
            resevation.reserved_end_date = data["reserved_end_date"]

            resevation.status = "Pending"
            resevation.created_at = datetime.now()

            db.session.add(resevation)
            db.session.flush()

            for room_id in data["room_ids"]:

                room = db.session.get(Room, room_id)

                if not room:
                    db.session.rollback()
                    return False, f"Room {room_id} not found"

                rr = ReservationRoom()

                rr.reservation_id = resevation.id
                rr.room_id = room_id

                rr.price_per_night = room.price

                db.session.add(rr)

            db.session.commit()

            return True, ReservationResponseSchema().dump(resevation)

        except Exception as ex:
            db.session.rollback()
            print(ex)
            return False, str(ex)

    @staticmethod
    def reservation_cancel(reservation_id):

        try:

            reservation = db.session.get(Reservation, reservation_id)

            if not reservation:
                return False, "Reservation not found"

            if reservation.status == "Checked-In":
                return False, (
                "Checked in reservation "
                "cannot be cancelled"
            )

            if reservation.status == "Checked-Out":
                return False, (
                "Checked out reservation "
                "cannot be cancelled"
            )

            if reservation.status == "Cancelled":
                return False, (
                "Reservation already cancelled"
            )

            reservation.status = "Cancelled"

            db.session.commit()

            return True, (
            ReservationResponseSchema()
            .dump(reservation)
        )

        except Exception as ex:

            db.session.rollback()

            return False, str(ex)