from Hotelguru.models.User import User
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.Room import Room
from Hotelguru.extensions import db
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reservation.schemas import ReservationSchema
from datetime import date



class ReceptionService:
    @staticmethod
    def check_in(reservation_id):
        try:
            reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
            if not reservation:
                return False, "Reservation not found"
            
            if reservation.status == "Cancelled":
                return False, "Reservation is already cancelled."

            if reservation.status == "Checked-In":
                return False, "Guest is already checked in."

            if reservation.reserved_start_date.date() > date.today():
                return False, "Too early check in."
            
            reservation.status = "Checked-In"
            db.session.commit()
            return True, ReservationSchema().dump(reservation)
        except Exception as e:
            db.session.rollback()
            return False, f"Something went wrong: {str(e)}"


#A tartózkodás végén a recepciós elvégzi a kijelentkezési (check-out) folyamatot, 
# és kiállítja a végszámlát, amely tartalmazza a szállásdíjat, valamint az igénybe vett extra szolgáltatások költségeit.
    @staticmethod
    def check_out(reservation_id):
        reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
        if not reservation:
            return False, "Reservation not found"
        
        if reservation.status == "Cancelled":
            return False, "Reservation cancelled"
        pass