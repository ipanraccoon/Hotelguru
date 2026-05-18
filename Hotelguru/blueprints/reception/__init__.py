from apiflask import APIBlueprint

bp = APIBlueprint('reception', __name__, tag="reception")

from Hotelguru.blueprints.reception import routes