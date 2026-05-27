from datetime import datetime
from Hotelguru.extensions import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

class HotelReview(db.Model):
        __tablename__ = "hotelreviews"

        id: Mapped[int] = mapped_column(primary_key=True)
        rating: Mapped[int] = mapped_column()
        comment: Mapped[str | None] = mapped_column(String(250), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime)
        user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
        hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))

        user: Mapped["User"] = relationship(back_populates="reviews")
        hotel: Mapped["Hotel"] = relationship(back_populates="reviews")
