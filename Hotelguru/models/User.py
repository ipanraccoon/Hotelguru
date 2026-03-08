from Hotelguru.extensions import db, Base
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
from typing import List

UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id"))
)

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    Name: Mapped[str] = mapped_column(String(30))
    Email: Mapped[str] = mapped_column(String(30))
    Password: Mapped[str] = mapped_column(String(30))
    Phone: Mapped[str] = mapped_column(String(30))

    roles: Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates = "users")