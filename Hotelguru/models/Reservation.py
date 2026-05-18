from datetime import datetime
from Hotelguru.extensions import db, Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List

class Reservation(db.Model):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reserved_start_date: Mapped[datetime] = mapped_column(DateTime)
    reserved_end_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    approver: Mapped["User"] = relationship(
        foreign_keys=[approved_by]
    )

    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="reservations")
    rooms: Mapped[List["ReservationRoom"]] = relationship(back_populates="reservation")
    invoice: Mapped["Invoice"] = relationship(back_populates="reservation")
    services: Mapped[List["ReservationService"]] = relationship(back_populates="reservation")