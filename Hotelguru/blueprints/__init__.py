from apiflask import APIBlueprint

apibp = APIBlueprint('api', __name__)

from Hotelguru.blueprints.user import bp as bp_user
apibp.register_blueprint(bp_user, url_prefix='/user')

from Hotelguru.blueprints.reception import bp as bp_reception
apibp.register_blueprint(bp_reception, url_prefix='/reception')

from Hotelguru.models import *