from Hotelguru.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean


class Room(db.Model):
    __tablename__="rooms"

    id: Mapped[int] = mapped_column(primary_key = True)
    Number: Mapped[int] = mapped_column(int)
    Beds: Mapped[int] = mapped_column(int)
    Kitchen: Mapped[bool] = mapped_column(bool)
    
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))