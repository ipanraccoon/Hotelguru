from flask import Flask
from Hotelguru.extensions import db
from flask_migrate import Migrate
from Hotelguru.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

from Hotelguru import models, views