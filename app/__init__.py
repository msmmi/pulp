
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

jwt = JWTManager(app)

from app import views, models


@jwt.user_claims_loader
def add_claims_to_access_token(email):
    session = db.session
    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        # todo log exception, there should be a user with this email here
        return {}
    return user.dict
