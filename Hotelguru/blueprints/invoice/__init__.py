from apiflask import APIBlueprint

bp = APIBlueprint(
    "invoice",
    __name__,
    url_prefix="/invoice",
    tag="invoice",
)

from Hotelguru.blueprints.invoice import routes
