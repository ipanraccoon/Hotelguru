from datetime import datetime
from Hotelguru.extensions import db
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
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    aproved_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="reservations")
    rooms: Mapped[List["ReservationRoom"]] = relationship(back_populates="reservation")