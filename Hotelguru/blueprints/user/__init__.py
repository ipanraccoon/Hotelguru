from apiflask import APIBlueprint

bp = APIBlueprint('user', __name__, tag="user")

from Hotelguru.blueprints.user import routes