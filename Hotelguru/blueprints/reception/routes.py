from Hotelguru.blueprints.reception import bp
from Hotelguru.blueprints.reception.service import ReceptionService
from Hotelguru.blueprints.reception.schemas import AddServiceSchema, ReservationServiceResponseSchema
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reservation.schemas import ReservationSchema
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Reception Blueprint'

@bp.put('/check_in/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.output(ReservationSchema)
def check_in(reservationid):
    success, response = ReceptionService.check_in(reservationid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/add_service/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.input(AddServiceSchema)
@bp.output(ReservationServiceResponseSchema)
def add_service(reservationid, json_data):
    success, response = ReceptionService.add_service(reservationid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/check_out/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.output(InvoiceSchema)
def check_out(reservationid):
    success, response = ReceptionService.check_out(reservationid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)