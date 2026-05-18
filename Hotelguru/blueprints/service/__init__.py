from apiflask import APIBlueprint

bp = APIBlueprint('service', __name__, tag="service")

from Hotelguru.blueprints.service import routes