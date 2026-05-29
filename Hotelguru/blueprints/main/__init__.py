from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="main")

from Hotelguru.blueprints.main import routes