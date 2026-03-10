from datetime import datetime
from Hotelguru.extensions import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List

class Invoice(db.Model):
    __tablename__="invoices"

    id: Mapped[int] = mapped_column(primary_key = True)
    total_amount: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime)

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"))
    issued_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    items: Mapped[List["InvoiceItem"]] = relationship(back_populates="invoice")
