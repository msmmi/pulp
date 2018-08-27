
from flask import Flask
from flask_jwt import JWT
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models


def authenticate(username, password):
    user = models.User.filter(models.User.username == username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return models.User.get(user_id)


jwt = JWT(app, authenticate, identity)
