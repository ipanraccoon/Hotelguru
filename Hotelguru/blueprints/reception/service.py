from Hotelguru.models.User import User
from Hotelguru.models.Reservation import Reservation
from Hotelguru.models.Room import Room
from Hotelguru.models.Invoice import Invoice
from Hotelguru.models.InvoiceItem import InvoiceItem
from Hotelguru.models.Service import Service
from Hotelguru.models.ReservationService import ReservationService
from Hotelguru.extensions import db
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reservation.schemas import ReservationSchema
from Hotelguru.blueprints.reception.schemas import ReservationServiceResponseSchema
from datetime import date, datetime


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


    @staticmethod
    def add_service(reservation_id, data):
        try:
            service_id = data["service_id"]
            quantity = data["quantity"] if "quantity" in data else 1

            reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
            if not reservation:
                return False, "Reservation not found"
            
            if reservation.status != "Checked-In":
                return False, "Services can only be added to checked-in guests."

            service = db.session.execute(db.select(Service).filter_by(id=service_id)).scalar_one_or_none()
            if not service:
                return False, "Service not found"

            res_service = ReservationService(
                reservation_id=reservation_id,
                service_id=service_id,
                quantity=quantity
            )
            db.session.add(res_service)
            db.session.commit()
            return True, ReservationServiceResponseSchema().dump(res_service)
        except Exception as e:
            db.session.rollback()
            return False, f"Something went wrong: {str(e)}"


    @staticmethod
    def check_out(reservation_id):
        reservation = db.session.execute(db.select(Reservation).filter_by(id=reservation_id)).scalar_one_or_none()
        if not reservation:
            return False, "Reservation not found"
        
        if reservation.status == "Cancelled":
            return False, "Reservation cancelled"
            
        if reservation.status != "Checked-In":
            return False, "Guest is not checked in"
            
        try:
            diff = reservation.reserved_end_date.date() - reservation.reserved_start_date.date()
            nights = diff.days if diff.days > 0 else 1
            
            total_amount = 0
            invoice_items = []
                       
            for room in reservation.rooms:
                room_total = room.price_per_night * nights
                total_amount += room_total
                
                item = InvoiceItem(
                    description=f"Szoba {room.room.number} - ({nights} éjszaka)",
                    amount=room_total
                )
                invoice_items.append(item)

            for res_service in reservation.services:
                service_price = res_service.service.price * res_service.quantity
                total_amount += service_price
                item = InvoiceItem(
                    description=f"Szolgáltatás: {res_service.service.name} ({res_service.quantity} db)",
                    amount=service_price
                )
                invoice_items.append(item)

            invoice = Invoice(
                total_amount=total_amount,
                created_at=datetime.now(),
                reservation_id=reservation.id,
                issued_by=1, #majd a recepcios id-je kell ide tokenbol
                items=invoice_items
            )
            
            reservation.status = "Checked-Out"
            db.session.add(invoice)
            db.session.commit()
            
            return True, InvoiceSchema().dump(invoice)
        except Exception as e:
            db.session.rollback()
            return False, f"Something went wrong: {str(e)}"