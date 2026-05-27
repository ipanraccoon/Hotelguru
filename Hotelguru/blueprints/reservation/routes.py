from Hotelguru.blueprints.reservation import bp
from Hotelguru.blueprints.reservation.schemas import ReservationRequestSchema, ReservationResponseSchema
from Hotelguru.blueprints.reservation.service import ReservationService


@bp.post('/add')
@bp.input(ReservationRequestSchema, location="json")
#@bp.output(ReservationResponseSchema)
def reservation_add(json_data):

    print(json_data)

    try:

     success, response = ReservationService.reservation_add(json_data)

     if success:
       return response, 200

     return {"message": response}, 400
    except Exception as ex:
        return {"ERROR": str(ex)}, 500

