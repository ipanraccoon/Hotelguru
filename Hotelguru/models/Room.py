from Hotelguru.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
from typing import List
from Hotelguru.models.RoomStatus import RoomStatus


class Room(db.Model):
    __tablename__="rooms"

    id: Mapped[int] = mapped_column(primary_key = True)
    number: Mapped[int] = mapped_column()
    beds: Mapped[int] = mapped_column()
    kitchen: Mapped[bool] = mapped_column()
    price: Mapped[int | None] = mapped_column(nullable=True)
    
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    status_id: Mapped[int | None] = mapped_column(
    ForeignKey("roomstatuses.id"),
    nullable=True
)

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    status: Mapped["RoomStatus"] = relationship(back_populates="rooms")
    reservations: Mapped[List["ReservationRoom"]] = relationship(back_populates="rooms")