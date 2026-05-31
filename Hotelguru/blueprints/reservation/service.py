from datetime import datetime, date, timedelta
from flask import current_app
from Hotelguru.extensions import db
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.ReservationRoom import ReservationRoom
from Hotelguru.models.Room import Room
from Hotelguru.blueprints.reservation.schemas import dump_reservation
from sqlalchemy import select, and_


class ReservationService:

    @staticmethod
    def _as_date(value):
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            return date.fromisoformat(value[:10])
        return value

    @staticmethod
    def _room_is_available(room_id, start_date, end_date):
        conflict = db.session.execute(
            select(ReservationRoom.id)
            .join(Reservation)
            .where(
                ReservationRoom.room_id == room_id,
                Reservation.status != "Cancelled",
                Reservation.reserved_start_date <= end_date,
                Reservation.reserved_end_date >= start_date,
            )
        ).first()
        return conflict is None

    @staticmethod
    def reservation_add(data, current_user_id=None, current_user_roles=None):
        try:
            if current_user_roles is None:
                current_user_roles = []
            if "Adminisztrátor" not in current_user_roles and data["user_id"] != current_user_id:
                return False, "Access denied"

            start_date = data["reserved_start_date"]
            end_date = data["reserved_end_date"]

            if start_date >= end_date:
                return False, "End date must be after start date"

            resevation = Reservation()

            resevation.user_id = data["user_id"]

            resevation.reserved_start_date = start_date
            resevation.reserved_end_date = end_date

            resevation.status = "Pending"
            resevation.created_at = datetime.now()

            db.session.add(resevation)
            db.session.flush()

            for room_id in data["room_ids"]:

                room = db.session.get(Room, room_id)

                if not room:
                    db.session.rollback()
                    return False, f"Room {room_id} not found"

                if not ReservationService._room_is_available(room_id, start_date, end_date):
                    db.session.rollback()
                    return False, f"Room {room_id} is not available for the selected dates"

                rr = ReservationRoom()

                rr.reservation_id = resevation.id
                rr.room_id = room_id

                rr.price_per_night = room.price

                db.session.add(rr)

            db.session.commit()

            return True, dump_reservation(resevation)

        except Exception as ex:
            db.session.rollback()
            print(ex)
            return False, str(ex)

    @staticmethod
    def get_user_reservations(user_id):
        reservations = db.session.execute(
            select(Reservation).filter_by(user_id=user_id).order_by(Reservation.id.desc())
        ).scalars().all()
        return True, dump_reservation(reservations, many=True)

    @staticmethod
    def get_reservation(reservation_id, user_id, roles=None):
        if roles is None:
            roles = []
        reservation = db.session.get(Reservation, reservation_id)
        if not reservation:
            return False, "Reservation not found"
        if reservation.user_id != user_id and "Adminisztrátor" not in roles and "Recepciós" not in roles:
            return False, "Access denied"
        return True, dump_reservation(reservation)

    @staticmethod
    def reservation_cancel(reservation_id, user_id=None):

        try:

            reservation = db.session.get(Reservation, reservation_id)

            if not reservation:
                return False, "Reservation not found"

            if user_id is not None and reservation.user_id != user_id:
                return False, "Access denied"

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

            start_date = ReservationService._as_date(reservation.reserved_start_date)
            deadline_days = current_app.config.get("CANCELLATION_DEADLINE_DAYS", 2)
            last_cancel_date = start_date - timedelta(days=deadline_days)
            if date.today() > last_cancel_date:
                return False, "Cancellation deadline has passed"

            reservation.status = "Cancelled"

            db.session.commit()

            return True, dump_reservation(reservation)

        except Exception as ex:

            db.session.rollback()

            return False, str(ex)