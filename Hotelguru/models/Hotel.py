from Hotelguru.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List


class Hotel(db.Model):
    __tablename__="hotels"

    id: Mapped[int] = mapped_column(primary_key = True)
    Name: Mapped[str] = mapped_column(String(30))
    City: Mapped[str] = mapped_column(String(30))
    Address: Mapped[str] = mapped_column(String(30))

    rooms: Mapped[List["Room"]] = relationship(backref="hotel")
    services: Mapped[List["Service"]] = relationship(back_populates="hotel")
