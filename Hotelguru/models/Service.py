from Hotelguru.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List



class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column()
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    
    hotel: Mapped["Hotel"] = relationship(back_populates="services")
    reservations: Mapped[List["ReservationService"]] = relationship(back_populates="service")