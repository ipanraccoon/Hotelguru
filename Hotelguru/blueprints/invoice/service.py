from Hotelguru.extensions import db
from Hotelguru.models.Invoice import Invoice
from Hotelguru.models.Reservation import Reservation
from Hotelguru.blueprints.invoice.schemas import dump_invoice
from sqlalchemy import select


class InvoiceService:
    @staticmethod
    def _can_view_invoice(invoice, user_id, roles):
        reservation = db.session.get(Reservation, invoice.reservation_id)
        if not reservation:
            return False
        if reservation.user_id == user_id:
            return True
        return "Adminisztrátor" in roles or "Recepciós" in roles

    @staticmethod
    def get_user_invoices(user_id):
        try:
            invoices = db.session.execute(
                select(Invoice)
                .join(Reservation, Invoice.reservation_id == Reservation.id)
                .where(Reservation.user_id == user_id)
                .order_by(Invoice.created_at.desc())
            ).scalars().all()
            return True, [dump_invoice(inv) for inv in invoices]
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def get_invoice(invoice_id, user_id, roles=None):
        if roles is None:
            roles = []
        try:
            invoice = db.session.get(Invoice, invoice_id)
            if not invoice:
                return False, "Invoice not found"
            if not InvoiceService._can_view_invoice(invoice, user_id, roles):
                return False, "Access denied"
            return True, dump_invoice(invoice)
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def get_invoice_by_reservation(reservation_id, user_id, roles=None):
        if roles is None:
            roles = []
        try:
            reservation = db.session.get(Reservation, reservation_id)
            if not reservation:
                return False, "Reservation not found"
            if reservation.user_id != user_id and "Adminisztrátor" not in roles and "Recepciós" not in roles:
                return False, "Access denied"
            invoice = db.session.execute(
                select(Invoice).where(Invoice.reservation_id == reservation_id)
            ).scalar_one_or_none()
            if not invoice:
                return False, "Invoice not found"
            return True, dump_invoice(invoice)
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
