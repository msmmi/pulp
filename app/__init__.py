
from flask import Flask
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views, models


def authenticate(username, password):
    session = db.session
    user = session.query(models.User).filter(models.User.username == username).first()
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    session = db.session
    return session.query(models.User).get(user_id)


jwt = JWT(app, authenticate, identity)
