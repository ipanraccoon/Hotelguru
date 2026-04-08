from Hotelguru.models.User import User
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.Room import Room
from Hotelguru.extensions import db
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema



class ReceptionService:
    @staticmethod
    def check_in(reservation_id):
        reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
        if not reservation:
            return False, "Reservation not found"
        #nincs kész
        pass

    @staticmethod
    def check_out(reservation_id):
        reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
        if not reservation:
            return False, "Reservation not found"
        
        if reservation.status == "Cancelled":
            return False, "Reservation cancelled"
        pass