from Hotelguru.blueprints.reservation import bp

from Hotelguru.blueprints.reservation.schemas import (
    ReservationRequestSchema,
    ReservationResponseSchema
)

from Hotelguru.blueprints.reservation.service import ReservationService


@bp.post('/add')
@bp.input(ReservationRequestSchema, location="json")
@bp.output(ReservationResponseSchema)
def reservation_add(json_data):

    success, response = ReservationService.reservation_add(json_data)

    if success:
        return response, 200

    return {"message": response}, 400
