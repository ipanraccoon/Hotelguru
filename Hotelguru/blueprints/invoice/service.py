from datetime import datetime
from Hotelguru.extensions import db
from Hotelguru.models.Invoice import Invoice
from Hotelguru.models.InvoiceItem import InvoiceItem
from Hotelguru.models.Reservation import Reservation

class InvoiceService:
    @staticmethod
    def invoice_generate(reservation_id, issued_by):
        try:
            reservation = db.session.get(Reservation, reservation_id)

            if not reservation:
                return False, "Reservation not found"
            if reservation.status != "Checked":
                pass
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)
