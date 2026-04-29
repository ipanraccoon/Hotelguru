from apiflask import Schema
from apiflask.fields import (
 Integer
)

class InvoiceRequestSchema(
 Schema
):
    reservation_id=Integer(
      required=True
    )

    issued_by=Integer(
      required=True
    )


class InvoiceResponseSchema(
 Schema
):
    id=Integer()
    total_amount=Integer()
