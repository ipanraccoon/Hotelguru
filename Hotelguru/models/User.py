from Hotelguru.extensions import db, Base
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash


UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id"))
)

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))

    reservations: Mapped[List["Reservation"]] = relationship(
    back_populates="user",
    foreign_keys="Reservation.user_id"
    )

    approved_reservations: Mapped[List["Reservation"]] = relationship(
    back_populates="approver",
    foreign_keys="Reservation.approved_by"
    )

    roles: Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates = "users")

    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
