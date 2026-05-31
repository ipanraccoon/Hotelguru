from Hotelguru.blueprints.reservation import bp
from Hotelguru.blueprints.reservation.schemas import ReservationRequestSchema, ReservationResponseSchema
from Hotelguru.blueprints.reservation.service import ReservationService
from Hotelguru.blueprints.reception.schemas import AddServiceSchema, ReservationServiceResponseSchema
from Hotelguru.extensions import auth
from Hotelguru.blueprints import role_required


@bp.post('/add')
@bp.input(ReservationRequestSchema, location="json")
@bp.auth_required(auth)
@role_required(["Vendég", "Adminisztrátor"])
def reservation_add(json_data):
    try:
        success, response = ReservationService.reservation_add(
            json_data,
            current_user_id=auth.current_user["user_id"],
            current_user_roles=[r["name"] for r in auth.current_user.get("roles", [])],
        )
        if success:
            return response, 200
        return {"message": response}, 400
    except Exception as ex:
        return {"ERROR": str(ex)}, 500


@bp.get('/mine')
@bp.auth_required(auth)
def reservation_mine():
    success, response = ReservationService.get_user_reservations(
        auth.current_user["user_id"]
    )
    if success:
        return response, 200
    return {"message": response}, 400


@bp.get('/<int:reservation_id>')
@bp.auth_required(auth)
def reservation_get(reservation_id):
    success, response = ReservationService.get_reservation(
        reservation_id,
        auth.current_user["user_id"],
        [r["name"] for r in auth.current_user.get("roles", [])],
    )
    if success:
        return response, 200
    return {"message": response}, 400


@bp.put('/cancel/<int:reservation_id>')
@bp.auth_required(auth)
def reservation_cancel(reservation_id):
    success, response = ReservationService.reservation_cancel(
        reservation_id,
        user_id=auth.current_user["user_id"],
    )

    if success:
        return response, 200

    return {"message": response}, 400


@bp.post('/add_service/<int:reservation_id>')
@bp.input(AddServiceSchema, location="json")
@bp.auth_required(auth)
@role_required(["Vendég"])
def reservation_add_service(reservation_id, json_data):
    success, response = ReservationService.add_service(
        reservation_id,
        json_data,
        auth.current_user["user_id"],
    )
    if success:
        return response, 200
    return {"message": response}, 400
