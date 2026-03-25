from Hotelguru.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
from typing import List


class Room(db.Model):
    __tablename__="rooms"

    id: Mapped[int] = mapped_column(primary_key = True)
    number: Mapped[int] = mapped_column()
    beds: Mapped[int] = mapped_column()
    kitchen: Mapped[bool] = mapped_column()
    
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    reservations: Mapped[List["ReservationRoom"]] = relationship(back_populates="room")