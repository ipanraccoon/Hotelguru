from Hotelguru.blueprints.Reservation import bp
from apiflask import APIBlueprint, HTTPError

from .schemas import (
    ReservationCreateSchema,
    ReservationResponseSchema
)

from Hotelguru.blueprints.Reservation.service import ReservationService




@bp.route('/')
def index():
    return "This is the Reservation blueprint"


@bp.post("/create")
@bp.doc(tags=["reservation"])
@bp.input(
    ReservationCreateSchema,
    location="json"
)
@bp.output(
    ReservationResponseSchema
)
def create_reservation(json_data):

    success,response = (
        ReservationService.create_reservation(
            json_data
        )
    )

    if success:
        return response,201

    raise HTTPError(
        message=response,
        status_code=400
    )


@bp.post("/approve/<int:id>")
@bp.doc(tags=["reservation"])
def approve_reservation(id):

    success,response = (
        ReservationService.approve_reservation(
            id
        )
    )

    if success:
        return response,200

    raise HTTPError(
        message=response,
        status_code=400
    )
