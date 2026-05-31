from Hotelguru.blueprints.invoice import bp
from Hotelguru.blueprints.invoice.service import InvoiceService
from Hotelguru.extensions import auth


@bp.get('/mine')
@bp.auth_required(auth)
def invoice_mine():
    success, response = InvoiceService.get_user_invoices(auth.current_user["user_id"])
    if success:
        return response, 200
    return {"message": response}, 400


@bp.get('/reservation/<int:reservation_id>')
@bp.auth_required(auth)
def invoice_by_reservation(reservation_id):
    success, response = InvoiceService.get_invoice_by_reservation(
        reservation_id,
        auth.current_user["user_id"],
        [r["name"] for r in auth.current_user.get("roles", [])],
    )
    if success:
        return response, 200
    return {"message": response}, 400


@bp.get('/<int:invoice_id>')
@bp.auth_required(auth)
def invoice_get(invoice_id):
    success, response = InvoiceService.get_invoice(
        invoice_id,
        auth.current_user["user_id"],
        [r["name"] for r in auth.current_user.get("roles", [])],
    )
    if success:
        return response, 200
    return {"message": response}, 400
