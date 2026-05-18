from apiflask import Schema, fields
from apiflask.fields import Integer, String, List, Nested


class InvoiceItemSchema(Schema):
    description = String()
    amount = Integer()

class InvoiceSchema(Schema):
    total_amount = Integer()
    items = Nested(InvoiceItemSchema, many=True)
    created_at = String()