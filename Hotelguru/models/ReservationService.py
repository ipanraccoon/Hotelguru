from Hotelguru.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ReservationService(db.Model):
    __tablename__ = "reservationservices"

    id: Mapped[int] = mapped_column(primary_key=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    quantity: Mapped[int] = mapped_column()

    reservation: Mapped["Reservation"] = relationship(back_populates="services")
    service: Mapped["Service"] = relationship(back_populates="reservations")
