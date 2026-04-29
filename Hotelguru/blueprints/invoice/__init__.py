from apiflask import APIBlueprint

bp = APIBlueprint('invoice', __name__, tag="invoice")


from Hotelguru.blueprints.invoice import routes
