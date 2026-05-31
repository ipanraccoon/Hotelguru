from datetime import datetime
from Hotelguru.extensions import db
from Hotelguru.models.Invoice import Invoice
from Hotelguru.models.Reservation import Reservation
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from sqlalchemy import select


class InvoiceService:
    @staticmethod
    def get_user_invoices(user_id):
        try:
            invoices = db.session.execute(
                select(Invoice)
                .join(Reservation, Invoice.reservation_id == Reservation.id)
                .where(Reservation.user_id == user_id)
                .order_by(Invoice.created_at.desc())
            ).scalars().all()
            return True, InvoiceSchema().dump(invoices, many=True)
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def invoice_generate(reservation_id, issued_by):
        try:
            reservation = db.session.get(Reservation, reservation_id)

            if not reservation:
                return False, "Reservation not found"
            if reservation.status != "Checked-In":
                return False, "Reservation must be checked in"
            return False, "Use reception check_out to generate invoices"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)
