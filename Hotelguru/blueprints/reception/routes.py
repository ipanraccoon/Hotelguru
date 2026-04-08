from Hotelguru.blueprints.reception import bp
from Hotelguru.blueprints.reception.service import ReceptionService
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Reception Blueprint'

@bp.put('/check_in')
@bp.doc(tags=["reception"])
@bp.input(ReservationSchema, location="json")
@bp.output(ReservationSchema)
def check_in():
    pass

@bp.get('/check_out/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.output(InvoiceSchema)
def check_out(reservationid):
    success, response = ReceptionService.check_out(reservationid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)