from datetime import datetime

from sqlalchemy import select

from Hotelguru.extensions import db

from Hotelguru.models.Invoice import Invoice
from Hotelguru.models.InvoiceItem import InvoiceItem
from Hotelguru.models.Reservation import Reservation

from .schemas import (
   InvoiceResponseSchema
)


class InvoiceService:


    @staticmethod
    def generate_invoice(request):

        try:

            reservation=(
                db.session.execute(
                    select(Reservation)
                    .filter_by(
                        id=request["reservation_id"]
                    )
                ).scalar_one()
            )


            nights=(
                reservation.reserved_end_date
                -
                reservation.reserved_start_date
            ).days


            total=0

            invoice=Invoice(
                reservation_id=reservation.id,
                issued_by=request["issued_by"],
                created_at=datetime.utcnow(),
                total_amount=0
            )

            db.session.add(
               invoice
            )

            db.session.flush()


            for room in reservation.rooms:

                amount=(
                    room.price_per_night
                    *
                    nights
                )

                total+=amount

                item=InvoiceItem(
                    description=
                    f"Room {room.room.number}",
                    amount=amount,
                    invoice_id=invoice.id
                )

                db.session.add(
                    item
                )


            invoice.total_amount=total

            db.session.commit()

        except Exception:
            db.session.rollback()
            return False,"Invoice generation failed"


        return (
            True,
            InvoiceResponseSchema().dump(
               invoice
            )
        )
