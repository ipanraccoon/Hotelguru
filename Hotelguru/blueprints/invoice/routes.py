from Hotelguru.blueprints.invoice import bp
from Hotelguru.blueprints.invoice.service import InvoiceService
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.extensions import auth


@bp.get('/mine')
@bp.auth_required(auth)
def invoice_mine():
    success, response = InvoiceService.get_user_invoices(auth.current_user["user_id"])
    if success:
        return response, 200
    return {"message": response}, 400
