from Hotelguru.blueprints.Reservation import bp
from Hotelguru.blueprints.Reservation.schemas import ReservationRequestSchema, ReservationResponseSchema
from Hotelguru.blueprints.Reservation.service import ReservationService
from Hotelguru.extensions import auth


@bp.post('/add')
@bp.input(ReservationRequestSchema, location="json")
def reservation_add(json_data):
    try:
        success, response = ReservationService.reservation_add(json_data)
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

