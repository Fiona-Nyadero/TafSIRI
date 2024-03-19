from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d-%m-%YT%H:%M'):
    if value is None:
        return ""
    return value.strftime(format)

from app import routes, models