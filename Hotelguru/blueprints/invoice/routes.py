from Hotelguru.blueprints.invoice import bp
from apiflask import APIBlueprint,HTTPError

from .schemas import (
   InvoiceRequestSchema,
   InvoiceResponseSchema
)

from Hotelguru.blueprints.invoice.service import InvoiceService




@bp.post("/generate")
@bp.doc(tags=["invoice"])
@bp.input(
   InvoiceRequestSchema,
   location="json"
)
@bp.output(
   InvoiceResponseSchema
)
def generate_invoice(
   json_data
):

    success,response=(
      InvoiceService.generate_invoice(
         json_data
      )
    )

    if success:
       return response,201

    raise HTTPError(
       message=response,
       status_code=400
    )
