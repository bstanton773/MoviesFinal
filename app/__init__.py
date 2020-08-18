from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_heroku import Heroku
heroku = Heroku(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_login import LoginManager
login = LoginManager(app)

from app import routes, models, user_routes