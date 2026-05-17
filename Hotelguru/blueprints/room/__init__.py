from apiflask import APIBlueprint

bp = APIBlueprint('room', __name__, tag="room")

from Hotelguru.blueprints.room import routes
