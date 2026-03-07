from Hotelguru.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean


class Role(db.Model):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    Name: Mapped[str] = mapped_column(String(30))
