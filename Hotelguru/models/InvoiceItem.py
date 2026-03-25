from Hotelguru.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

class InvoiceItem(db.Model):
    __tablename__ = "invoiceitems"

    id: Mapped[int] = mapped_column(primary_key = True)
    description: Mapped[str] = mapped_column(String(30))
    amount: Mapped[int] = mapped_column()

    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))

    invoice: Mapped["Invoice"] = relationship(back_populates="items")
