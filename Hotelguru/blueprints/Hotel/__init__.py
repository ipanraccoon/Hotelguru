from apiflask import APIBlueprint

bp = APIBlueprint('hotel', __name__, tag="hotel")

from app.bluprints.hotel import routes
