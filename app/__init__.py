from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "sqlite:///films.db"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = 'Необходимо авторизоваться!'
# login_manager.login_message_category = 'alert-warning'

from . import models, views

db.create_all()
