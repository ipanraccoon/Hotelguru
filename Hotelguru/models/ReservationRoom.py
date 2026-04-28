from datetime import datetime
from Hotelguru.extensions import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List

class ReservationRoom(db.Model):
    __tablename__ = "reservationrooms"

    id: Mapped[int] = mapped_column(primary_key = True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    price_per_night: Mapped[int] = mapped_column()

    reservation: Mapped["Reservation"] = relationship(back_populates="rooms")
    rooms: Mapped["Room"] = relationship(back_populates="reservations")
