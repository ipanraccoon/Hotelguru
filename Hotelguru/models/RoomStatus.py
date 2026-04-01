from Hotelguru.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
from typing import List

class Role(db.Model):
    __tablename__="roomstatuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    rooms: Mapped[List["Rooms"]] = relationship(back_populates="roomstatuses")

