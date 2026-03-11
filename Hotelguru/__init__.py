from flask import Flask
from Hotelguru.extensions import db
from flask_migrate import Migrate
from Hotelguru.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    migrate = Migrate(app, db)
    
    from Hotelguru.views import bp
    app.register_blueprint(bp)
    return app

from Hotelguru import models, views