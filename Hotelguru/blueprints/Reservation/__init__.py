from apiflask import APIBlueprint

bp = APIBlueprint('reservation', __name__, tag="reservation")


from Hotelguru.blueprints.Reservation import routes
