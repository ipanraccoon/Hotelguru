from apiflask import APIFlask
from Hotelguru.extensions import db
from flask_migrate import Migrate
from Hotelguru.config import Config

def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors=True, docs_path="/swagger", title="Hotelguru")
    app.config["JSON_AS_ASCII"] = False
    app.config.from_object(config_class)
    
    db.init_app(app)

    migrate = Migrate(app, db)
    
    # from Hotelguru.views import bp as main_bp
    # app.register_blueprint(main_bp)

    from Hotelguru.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from Hotelguru.blueprints.room import bp as room_bp
    app.register_blueprint(room_bp)

    from Hotelguru.blueprints.Hotel import bp as hotel_bp
    app.register_blueprint(hotel_bp)

    from Hotelguru.blueprints.user import bp as bp_user
    app.register_blueprint(bp_user)

    from Hotelguru.blueprints.reception import bp as bp_reception
    app.register_blueprint(bp_reception)

    from Hotelguru.blueprints.service import bp as bp_service
    app.register_blueprint(bp_service)

    from Hotelguru.blueprints.Reservation import bp as bp_reservation
    app.register_blueprint(bp_reservation)

    from Hotelguru.blueprints.invoice import bp as bp_invoice
    app.register_blueprint(bp_invoice)

    return app

from Hotelguru import models, views