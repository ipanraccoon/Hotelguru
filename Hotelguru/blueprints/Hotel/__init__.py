from apiflask import APIBlueprint

bp = APIBlueprint('hotel', __name__, tag="hotel")

from Hotelguru.blueprints.Hotel import routes
