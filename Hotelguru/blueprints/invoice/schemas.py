from datetime import datetime, date
from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested


def _format_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def dump_invoice(invoice):
    return {
        "id": invoice.id,
        "reservation_id": invoice.reservation_id,
        "total_amount": invoice.total_amount,
        "items": [
            {"description": item.description, "amount": item.amount}
            for item in invoice.items
        ],
        "created_at": _format_datetime(invoice.created_at),
    }


class InvoiceItemSchema(Schema):
    description = String()
    amount = Integer()

class InvoiceSchema(Schema):
    id = Integer()
    reservation_id = Integer()
    total_amount = Integer()
    items = Nested(InvoiceItemSchema, many=True)
    created_at = String()