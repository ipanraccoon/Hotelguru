from hmac import new
from Hotelguru.blueprints.reception import bp
from Hotelguru.blueprints.reception.service import ReceptionService
from Hotelguru.blueprints.reception.schemas import AddServiceSchema, ReservationServiceResponseSchema
from Hotelguru.blueprints.invoice.schemas import InvoiceSchema
from Hotelguru.blueprints.reservation.schemas import ReservationResponseSchema
from apiflask import HTTPError
from Hotelguru.extensions import auth
from Hotelguru.blueprints import role_required


@bp.put('/check_in/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
#@bp.output(ReservationResponseSchema)
def check_in(reservationid):
    try:
        success, response = ReceptionService.check_in(reservationid)
        if success:
            return response, 200
        return {"message": response}, 400
    except Exception as ex:
        return {"ERROR": str(ex)}, 500

@bp.get('/reservations/pending')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
def pending_reservations():
    success, response = ReceptionService.get_pending_reservations()
    if success:
        return response, 200
    return {"message": response}, 400


@bp.put('/approve/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
def approve_reservation(reservationid):
    success, response = ReceptionService.approve_reservation(
        reservationid,
        auth.current_user["user_id"],
    )
    if success:
        return response, 200
    return {"message": response}, 400


@bp.put('/reject/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
def reject_reservation(reservationid):
    success, response = ReceptionService.reject_reservation(reservationid)
    if success:
        return response, 200
    return {"message": response}, 400


@bp.post('/add_service/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
@bp.input(AddServiceSchema)
@bp.output(ReservationServiceResponseSchema)
def add_service(reservationid, json_data):
    success, response = ReceptionService.add_service(reservationid, json_data)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/check_out/<int:reservationid>')
@bp.doc(tags=["reception"])
@bp.auth_required(auth)
@role_required(["Recepciós"])
#@bp.output(InvoiceSchema)
def check_out(reservationid):
    try:
        success, response = ReceptionService.check_out(reservationid)
        if success:
            return response, 200
        return {"message": response}, 400
    except Exception as ex:
        return {"ERROR": str(ex)}, 500