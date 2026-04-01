from apiflask import APIFlask
from Hotelguru.extensions import db
from flask_migrate import Migrate
from Hotelguru.config import Config

def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors=True, docs_path="/swagger", title="Hotelguru")
    app.config.from_object(config_class)
    
    db.init_app(app)

    migrate = Migrate(app, db)
    
    from Hotelguru.views import bp
    app.register_blueprint(bp)
    from Hotelguru.blueprints import apibp
    app.register_blueprint(apibp, url_prefix="/api")


    return app

from Hotelguru import models, views