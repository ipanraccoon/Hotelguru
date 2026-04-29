from apiflask import APIBlueprint

apibp = APIBlueprint('api', __name__)

from Hotelguru.blueprints.Reservation import bp as bp_reservation
apibp.register_blueprint(bp_reservation, url_prefix='/reservation')

from Hotelguru.blueprints.invoice import bp as bp_invoice
apibp.register_blueprint(bp_invoice, url_prefix='/invoice')


from Hotelguru.models import *
