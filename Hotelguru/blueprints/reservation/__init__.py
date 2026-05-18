from apiflask import APIBlueprint

bp = APIBlueprint(
    "reservation",
    __name__,
    url_prefix="/reservation",
    tag="Reservation"
)

from Hotelguru.blueprints.reservation import routes
